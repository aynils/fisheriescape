from copy import deepcopy

from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from pandas import date_range
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from dm_apps.utils import custom_send_mail
from shared_models import models as shared_models
from shared_models.utils import get_labels
from . import permissions, pagination
from . import serializers
from .. import models, stat_holidays, emails
from ..filters import ProjectYearChildFilter, ProjectYearFilter
from ..utils import financial_project_year_summary_data, financial_project_summary_data, get_user_fte_breakdown, can_modify_project, \
    get_manageable_sections, multiple_financial_project_year_summary_data, is_section_head
from ..utils import is_management_or_admin


# Functional API Views
############


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserDisplaySerializer(instance=request.user)
        data = serializer.data
        if request.query_params.get("project"):
            data.update(can_modify_project(request.user, request.query_params.get("project"), True))

        if request.query_params.get("status_report"):
            status_report = get_object_or_404(models.StatusReport, pk=request.query_params.get("status_report"))
            data.update(can_modify_project(request.user, status_report.project_year.project_id, True))
            data.update(dict(is_section_head=is_section_head(request.user, status_report.project_year.project)))
        return Response(data)


class FTEBreakdownAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # if there are no project year ids, do this
        if not request.query_params.get("ids"):
            # if no user is specified, we will assume it is the request user
            if not request.query_params.get("user"):
                my_user = request.user
            else:
                my_user = get_object_or_404(User, pk=request.query_params.get("user"))

            # if there is no fiscal year specified, let's get all years
            if not request.query_params.get("year"):
                # need a list of fiscal years
                fy_qs = shared_models.FiscalYear.objects.filter(projectyear__staff__user=my_user).distinct()
                data = list()
                for fy in fy_qs:
                    data.append(get_user_fte_breakdown(my_user, fiscal_year_id=fy.id))
            else:
                data = get_user_fte_breakdown(my_user, fiscal_year_id=request.query_params.get("year"))
            return Response(data, status.HTTP_200_OK)
        else:
            if not request.query_params.get("year"):
                return Response({"error": "must supply a fiscal year"}, status.HTTP_400_BAD_REQUEST)

            data = list()
            ids = request.query_params.get("ids").split(",")
            year = request.query_params.get("year")
            # now we need a user list for any users in the above list
            users = User.objects.filter(staff_instances2__project_year_id__in=ids).distinct().order_by("last_name")

            for u in users:
                my_dict = get_user_fte_breakdown(u, fiscal_year_id=year)
                staff_instances = models.Staff.objects.filter(user=u, project_year__fiscal_year_id=year).distinct()
                my_dict["staff_instances"] = serializers.StaffSerializer(staff_instances, many=True).data
                data.append(my_dict)

            return Response(data, status.HTTP_200_OK)


class FinancialsAPIView(APIView):
    permissions = [IsAuthenticated]

    def get(self, request):
        qp = request.query_params
        if qp.get("ids"):
            ids = request.query_params.get("ids").split(",")  # get project year list
            project_years = models.ProjectYear.objects.filter(id__in=ids)  # get project year qs
            data = multiple_financial_project_year_summary_data(project_years)
            return Response(data, status.HTTP_200_OK)
        elif qp.get("project_year"):
            obj = get_object_or_404(models.ProjectYear, pk=qp.get("project_year"))
            data = financial_project_year_summary_data(obj)
            return Response(data, status.HTTP_200_OK)
        elif qp.get("project"):
            obj = get_object_or_404(models.Project, pk=qp.get("project"))
            data = financial_project_summary_data(obj)
            return Response(data, status.HTTP_200_OK)


class GetDatesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fiscal_year = self.request.query_params.get("year")  # to be formatted as follows: YYYY; SAP style
        if fiscal_year:
            fiscal_year = int(fiscal_year)
            # create a pandas date_range object for upcoming fiscal year
            start = f"{fiscal_year - 1}-04-01"
            end = f"{fiscal_year}-03-31"
            datelist = date_range(start=start, end=end).tolist()

            date_format = "%d-%B-%Y"
            short_date_format = "%d-%b-%Y"
            # get a list of statutory holidays
            holiday_list = [d.strftime(date_format) for d in stat_holidays.stat_holiday_list]

            data = list()
            # create a dict for the response
            for dt in datelist:
                is_stat = dt.strftime(date_format) in holiday_list
                weekday = dt.strftime("%A")
                int_weekday = dt.strftime("%w")
                obj = dict(
                    formatted_date=dt.strftime(date_format),
                    formatted_short_date=dt.strftime(short_date_format),
                    weekday=weekday,
                    short_weekday=f'{dt.strftime("%a")}.',
                    int_weekday=int_weekday,
                    is_stat=is_stat,
                    pay_rate=2 if is_stat or int_weekday == 0 else 1.5
                )
                data.append(obj)
            return Response(data, status.HTTP_200_OK)
        raise ValidationError("missing query parameter 'year'")


class ProjectViewSet(ModelViewSet):
    queryset = models.Project.objects.all().order_by("id")
    serializer_class = serializers.ProjectSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("id",)

    def list(self, request, *args, **kwargs):
        # if not admin user, hidden projects should not be included in the qs
        if not is_management_or_admin(self.request.user):
            self.queryset = self.queryset.filter(is_hidden=False)
        return super().list(request, *args, **kwargs)

    def post(self, request, pk):
        qp = request.query_params
        project = get_object_or_404(models.Project, pk=pk)
        if qp.get("action") and not qp.get("citation"):
            action = qp.get("action")
            citation = get_object_or_404(shared_models.Citation, pk=qp.get("citation"))
            if action == "add":
                project.references.add(citation)
            elif action == "remove":
                project.references.remove(citation)
            return Response(serializers.CitationSerializer(citation).data, status=status.HTTP_200_OK)
        raise ValidationError(_("This endpoint cannot be used without a query param"))


class ProjectYearViewSet(ModelViewSet):
    queryset = models.ProjectYear.objects.all().order_by("start_date")
    serializer_class = serializers.ProjectYearSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectYearFilter

    def list(self, request, *args, **kwargs):
        qp = request.query_params
        # if not admin user, hidden projects should not be included in the qs
        if not is_management_or_admin(self.request.user):
            self.queryset = self.queryset.filter(project__is_hidden=False, status__in=[2, 3, 4])
        # if the user param is present, it means we are looking at the My Projects page.
        if qp.get("user"):
            self.queryset = self.queryset.filter(project__section__in=get_manageable_sections(request.user)).order_by("fiscal_year", "project_id")
        return super().list(request, *args, **kwargs)

    def post(self, request, pk):
        qp = request.query_params
        project_year = get_object_or_404(models.ProjectYear, pk=pk)
        if qp.get("submit"):
            project_year.submit(request)
            # create a new email object
            email = emails.ProjectYearSubmissionEmail(project_year, request)
            # send the email object
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )
            return Response(serializers.ProjectYearSerializer(project_year).data, status.HTTP_200_OK)
        elif qp.get("unsubmit"):
            project_year.unsubmit(request)
            return Response(serializers.ProjectYearSerializer(project_year).data, status.HTTP_200_OK)
        elif qp.get("add-all-costs"):
            project_year.add_all_om_costs()
            project_year.update_modified_by(request.user)
            serializer = serializers.OMCostSerializer(instance=project_year.omcost_set.all(), many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        elif qp.get("remove-empty-costs"):
            project_year.clear_empty_om_costs()
            project_year.update_modified_by(request.user)
            serializer = serializers.OMCostSerializer(instance=project_year.omcost_set.all(), many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        raise ValidationError(_("This endpoint cannot be used without a query param"))


class StaffViewSet(ModelViewSet):
    queryset = models.Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "project_year"
    ]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        staff = get_object_or_404(models.Staff, pk=self.kwargs.get("pk"))
        old_lead_status = staff.is_lead
        staff = serializer.save()
        staff.project_year.update_modified_by(self.request.user)
        if (old_lead_status is False and staff.is_lead) and (staff.user and staff.user.email):
            email = emails.StaffEmail(staff, "add", self.request)
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )
        super().perform_update(serializer)

    def perform_create(self, serializer):
        staff = serializer.save()
        staff.project_year.update_modified_by(self.request.user)
        if staff.user and staff.user.email:
            email = emails.StaffEmail(staff, "add", self.request)
            custom_send_mail(
                subject=email.subject,
                html_message=email.message,
                from_email=email.from_email,
                recipient_list=email.to_list
            )


class OMCostViewSet(ModelViewSet):
    serializer_class = serializers.OMCostSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    queryset = models.OMCost.objects.all()
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProjectYearChildFilter

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)


class CapitalCostViewSet(ModelViewSet):
    serializer_class = serializers.CapitalCostSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    queryset = models.CapitalCost.objects.all()
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProjectYearChildFilter

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)


class ActivityViewSet(ModelViewSet):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProjectYearChildFilter

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)

    def post(self, request, pk):
        # we only allow this method when we are changing statuses
        qp = request.GET
        action = qp.get("action")
        clone = qp.get("clone")
        if action == "complete" or action == "incomplete":
            activity = get_object_or_404(models.Activity, pk=pk)
            # get or create a status report
            qs = models.StatusReport.objects.filter(project_year=activity.project_year)
            if qs:
                status_report = qs.order_by("id").last()
            else:
                status_report = models.StatusReport.objects.create(project_year=activity.project_year)
            # now we get or create the activity update
            update, create = models.ActivityUpdate.objects.get_or_create(
                status_report=status_report,
                activity=activity,
            )
            if action == "complete":
                update.status = 8
            else:
                update.status = 7
            update.notes = request.data
            update.save()
            return Response(serializers.ActivitySerializer(activity).data, status=status.HTTP_200_OK)
        elif clone:
            old_activity = get_object_or_404(models.Activity, pk=pk)
            new_activity = deepcopy(old_activity)
            new_activity.pk = None
            new_activity.save()
            return Response(serializers.ActivitySerializer(new_activity).data, status=status.HTTP_200_OK)
        raise ValidationError("sorry, I am missing the query param for 'action' or 'clone'")


class CollaborationViewSet(ModelViewSet):
    queryset = models.Collaboration.objects.all()
    serializer_class = serializers.CollaborationSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProjectYearChildFilter

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)


class CitationViewSet(ModelViewSet):
    queryset = shared_models.Citation.objects.all()
    serializer_class = serializers.CitationSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]  # This might have to be looked at
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = [
        "name",
        "nom",
        "authors",
        "abstract_en",
        "abstract_fr",
    ]
    filterset_fields = [
        "projects",
    ]

    def perform_update(self, serializer):
        obj = serializer.save()
        # if there is a new publication being passed in... create it and then add it to citation
        if self.request.data.get("new_publication") and self.request.data.get("new_publication") != "":
            pub, created = shared_models.Publication.objects.get_or_create(name=self.request.data.get("new_publication"))
            obj.publication = pub
            obj.save()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

    def perform_create(self, serializer):
        obj = serializer.save()

        if self.request.data.get("new_publication") and self.request.data.get("new_publication") != "":
            pub, created = shared_models.Publication.objects.get_or_create(name=self.request.data.get("new_publication"))
            obj.publication = pub
            obj.save()

        if self.request.query_params.get("project"):
            project = get_object_or_404(models.Project, pk=self.request.query_params.get("project"))
            project.references.add(obj)
            project.modified_by = self.request.user
            project.save()


class StatusReportViewSet(ModelViewSet):
    queryset = models.StatusReport.objects.all()
    serializer_class = serializers.StatusReportSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProjectYearChildFilter

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)


class ActivityUpdateViewSet(ModelViewSet):
    queryset = models.ActivityUpdate.objects.all()
    serializer_class = serializers.ActivityUpdateSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = [
        "status_report",
        "status_report__project_year",
    ]

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.status_report.project_year.update_modified_by(self.request.user)


class FileViewSet(ModelViewSet):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = [
        "status_report",
        "project_year",
        "project",
    ]

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        instance.project_year.update_modified_by(self.request.user)

    def perform_update(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.project_year.update_modified_by(self.request.user)


class ReviewViewSet(ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProjectYearChildFilter

    def perform_update(self, serializer):
        obj = serializer.save(last_modified_by=self.request.user)
        obj.project_year.update_modified_by(self.request.user)
        data = self.request.data
        if data.get("approval_email_update"):
            obj.send_approval_email(self.request)
        elif data.get("review_email_update"):
            obj.send_review_email(self.request)

    def perform_create(self, serializer):
        obj = serializer.save(last_modified_by=self.request.user)
        obj.project_year.update_modified_by(self.request.user)
        data = self.request.data
        if data.get("approval_email_update"):
            obj.send_approval_email(self.request)
        elif data.get("review_email_update"):
            obj.send_review_email(self.request)


# LOOKUPS
##########

class FiscalYearListAPIView(ListAPIView):
    serializer_class = serializers.FiscalYearSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = shared_models.FiscalYear.objects.filter(projectyear__isnull=False)
        if self.request.query_params.get("user") == 'true':
            qs = qs.filter(projectyear__project__section__in=get_manageable_sections(self.request.user))
        return qs.distinct()


class TagListAPIView(ListAPIView):
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = models.Tag.objects.filter(projects__isnull=False)
        if self.request.query_params.get("user") == 'true':
            qs = qs.filter(projects__section__in=get_manageable_sections(self.request.user))
        return qs.distinct()


class ThemeListAPIView(ListAPIView):
    serializer_class = serializers.ThemeSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = models.Theme.objects.all()
        if self.request.query_params.get("user") == 'true':
            qs = qs.filter(functional_groups__projects__section__in=get_manageable_sections(self.request.user))
        return qs.distinct()


class FunctionalGroupListAPIView(ListAPIView):
    serializer_class = serializers.FunctionalGroupSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = [
        "sections",
        "sections__division",
        "sections__division__branch__sector__region",
    ]

    def get_queryset(self):
        qs = models.FunctionalGroup.objects.all()
        if self.request.query_params.get("user") == 'true':
            qs = qs.filter(sections__in=get_manageable_sections(self.request.user))
        return qs.distinct()


class FundingSourceListAPIView(ListAPIView):
    serializer_class = serializers.FundingSourceSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = models.FundingSource.objects.all()
        if self.request.query_params.get("user") == 'true':
            qs = qs.filter(projects__section__in=get_manageable_sections(self.request.user))
        return qs.distinct()


class RegionListAPIView(ListAPIView):
    serializer_class = serializers.RegionSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]

    def get_queryset(self):
        qs = shared_models.Region.objects.filter(branches__divisions__sections__ppt__isnull=False)
        # if there is a user param, further filter qs to what user can access
        if self.request.query_params.get("user"):
            qs = qs.filter(branches__divisions__sections__in=get_manageable_sections(self.request.user))
        return qs.distinct()


class DivisionListAPIView(ListAPIView):
    serializer_class = serializers.DivisionSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = [
        "branch__sector__region",
    ]

    def get_queryset(self):
        qs = shared_models.Division.objects.filter(sections__ppt__isnull=False).distinct()
        # if there is a user param, further filter qs to what user can access
        if self.request.query_params.get("user"):
            qs = qs.filter(sections__in=get_manageable_sections(self.request.user))
        return qs.distinct()


class SectionListAPIView(ListAPIView):
    serializer_class = serializers.SectionSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = [
        "division",
        "division__branch__sector__region",
    ]

    def get_queryset(self):
        qs = shared_models.Section.objects.filter(ppt__isnull=False).distinct()
        # if there is a user param, further filter qs to what user can access
        if self.request.query_params.get("user"):
            qs = qs.filter(id__in=[s.id for s in get_manageable_sections(self.request.user)])
        return qs


class PublicationListAPIView(ListAPIView):
    queryset = shared_models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    permission_classes = [permissions.CanModifyOrReadOnly]


class ActivityModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.Activity

    def get(self, request):
        data = dict()
        data['labels'] = get_labels(self.model)
        data['type_choices'] = [dict(text=item[1], value=item[0]) for item in models.Activity.type_choices]
        data['likelihood_choices'] = [dict(text=item[1], value=item[0]) for item in models.Activity.likelihood_choices]
        data['impact_choices'] = [dict(text=item[1], value=item[0]) for item in models.Activity.impact_choices]
        data['risk_rating_choices'] = [dict(text=item[1], value=item[0]) for item in models.Activity.risk_rating_choices]
        return Response(data)


class OMCostModelMetaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    model = models.OMCost

    def get(self, request):
        data = dict()
        data['labels'] = get_labels(self.model)
        data['om_category_choices'] = [dict(text=item.id, value=str(item)) for item in models.OMCategory.objects.all()]
        return Response(data)
