from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.template.defaultfilters import date, slugify
from django.urls import reverse
from django.utils.translation import gettext as _
from markdown import markdown
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from lib.functions.custom_functions import listrify
from lib.templatetags.custom_filters import nz
from shared_models import models as shared_models
from .. import models
from ..utils import can_modify_project, in_ppt_admin_group, is_management, is_rds


class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "is_admin", "is_management", "is_rds"]

    is_admin = serializers.SerializerMethodField()
    is_management = serializers.SerializerMethodField()
    is_rds = serializers.SerializerMethodField()

    def get_is_admin(self, instance):
        return in_ppt_admin_group(instance)

    def get_is_management(self, instance):
        return is_management(instance)

    def get_is_rds(self, instance):
        return is_rds(instance)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = "__all__"

    metadata = serializers.SerializerMethodField()
    general_comment_html = serializers.SerializerMethodField()
    approval_notification_email_sent = serializers.SerializerMethodField()
    review_notification_email_sent = serializers.SerializerMethodField()
    collaboration_score_html = serializers.SerializerMethodField()
    strategic_score_html = serializers.SerializerMethodField()
    operational_score_html = serializers.SerializerMethodField()
    ecological_score_html = serializers.SerializerMethodField()
    scale_score_html = serializers.SerializerMethodField()
    approval_level_display = serializers.SerializerMethodField()
    approval_status_display = serializers.SerializerMethodField()
    funding_status_display = serializers.SerializerMethodField()

    def get_funding_status_display(self, instance):
        return instance.get_funding_status_display()

    def get_approval_status_display(self, instance):
        return instance.get_approval_status_display()

    def get_approval_level_display(self, instance):
        return instance.get_approval_level_display()

    def get_scale_score_html(self, instance):
        return instance.scale_score_html

    def get_ecological_score_html(self, instance):
        return instance.ecological_score_html

    def get_operational_score_html(self, instance):
        return instance.operational_score_html

    def get_strategic_score_html(self, instance):
        return instance.strategic_score_html

    def get_collaboration_score_html(self, instance):
        return instance.collaboration_score_html

    def get_approval_notification_email_sent(self, instance):
        return date(instance.approval_notification_email_sent)

    def get_review_notification_email_sent(self, instance):
        return date(instance.review_notification_email_sent)

    def get_metadata(self, instance):
        return instance.metadata

    def get_general_comment_html(self, instance):
        return instance.general_comment_html


class ProjectYearSerializerLITE(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectYear
        fields = [
            "id",
            "status",
            "project",
            "display_name",
            "submitted",
            "status_class",
            "status_display",
            "formatted_status",
            "project_title",
            "project_section",
        ]

    display_name = serializers.SerializerMethodField()
    submitted = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    status_class = serializers.SerializerMethodField()
    formatted_status = serializers.SerializerMethodField()
    project_title = serializers.SerializerMethodField()
    project_section = serializers.SerializerMethodField()

    def get_project_section(self, instance):
        return str(instance.project.section)

    def get_project_title(self, instance):
        return instance.project.title

    def get_formatted_status(self, instance):
        return instance.formatted_status

    def get_status_class(self, instance):
        return slugify(instance.get_status_display())

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_display_name(self, instance):
        return str(instance.fiscal_year)

    def get_submitted(self, instance):
        if instance.submitted:
            return instance.submitted.strftime("%Y-%m-%d")


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        exclude = ["updated_at", ]

    years = ProjectYearSerializerLITE(many=True, read_only=True)
    has_unsubmitted_years = serializers.SerializerMethodField()
    section = serializers.StringRelatedField()
    functional_group = serializers.StringRelatedField()
    default_funding_source = serializers.StringRelatedField()
    lead_staff = serializers.SerializerMethodField()
    start_year_display = serializers.SerializerMethodField()
    tags_display = serializers.SerializerMethodField()
    funding_sources_display = serializers.SerializerMethodField()
    section_display = serializers.SerializerMethodField()

    def get_section_display(self, instance):
        return instance.section.full_name

    def get_funding_sources_display(self, instance):
        if instance.funding_sources.exists():
            return listrify(instance.funding_sources.all())

    def get_tags_display(self, instance):
        if instance.tags.exists():
            return listrify(instance.tags.all())

    def get_has_unsubmitted_years(self, instance):
        return instance.has_unsubmitted_years

    def get_lead_staff(self, instance):
        return listrify([str(nz(s)) for s in instance.lead_staff.all()])

    def get_start_year_display(self, instance):
        if instance.starting_fy:
            return str(instance.starting_fy)


class ProjectYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectYear
        exclude = ["updated_at", ]

    project = ProjectSerializer(read_only=True)
    review = ReviewSerializer(read_only=True)
    display_name = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()
    metadata = serializers.SerializerMethodField()
    last_modified = serializers.SerializerMethodField()
    can_modify = serializers.SerializerMethodField()
    submitted = serializers.SerializerMethodField()

    deliverables_html = serializers.SerializerMethodField()
    priorities_html = serializers.SerializerMethodField()
    technical_service_needs_html = serializers.SerializerMethodField()
    mobilization_needs_html = serializers.SerializerMethodField()
    vehicle_needs_html = serializers.SerializerMethodField()
    ship_needs_html = serializers.SerializerMethodField()
    field_staff_needs_html = serializers.SerializerMethodField()
    instrumentation_html = serializers.SerializerMethodField()
    data_collected_html = serializers.SerializerMethodField()
    data_products_html = serializers.SerializerMethodField()
    data_storage_plan_html = serializers.SerializerMethodField()
    data_management_needs_html = serializers.SerializerMethodField()
    other_lab_support_needs_html = serializers.SerializerMethodField()
    it_needs_html = serializers.SerializerMethodField()
    default_funding_source_id = serializers.SerializerMethodField()
    formatted_status = serializers.SerializerMethodField()
    allocated_budget = serializers.SerializerMethodField()
    review_score_percentage = serializers.SerializerMethodField()
    review_score_fraction = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    status_class = serializers.SerializerMethodField()
    om_costs = serializers.SerializerMethodField()
    salary_costs = serializers.SerializerMethodField()
    capital_costs = serializers.SerializerMethodField()
    om_allocations = serializers.SerializerMethodField()
    salary_allocations = serializers.SerializerMethodField()
    capital_allocations = serializers.SerializerMethodField()
    project_codes = serializers.SerializerMethodField()
    project_user_choices = serializers.SerializerMethodField()
    parent_activity_choices = serializers.SerializerMethodField()

    services = serializers.SerializerMethodField()

    def get_services(self, instance):
        if instance.services.exists():
            return listrify(instance.services.all())

    def get_parent_activity_choices(self, instance):
        return [dict(id=obj.id, value=f"{obj.get_type_display()} - {obj}") for obj in instance.activities.filter(parent__isnull=True)]

    def get_project_user_choices(self, instance):
        project_users = User.objects.filter(staff_instances2__project_year__project=instance.project).distinct()
        return [dict(id=obj.id, value=str(obj)) for obj in project_users]

    def get_project_codes(self, instance):
        return instance.project_codes

    def get_capital_costs(self, instance):
        return instance.capital_costs

    def get_salary_costs(self, instance):
        return instance.salary_costs

    def get_om_costs(self, instance):
        return instance.om_costs
    
    def get_capital_allocations(self, instance):
        return instance.capital_allocations

    def get_salary_allocations(self, instance):
        return instance.salary_allocations

    def get_om_allocations(self, instance):
        return instance.om_allocations

    def get_status_class(self, instance):
        return slugify(instance.get_status_display())

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_review_score_percentage(self, instance):
        return instance.review_score_percentage

    def get_review_score_fraction(self, instance):
        return instance.review_score_fraction

    def get_allocated_budget(self, instance):
        return instance.allocated_budget

    def get_display_name(self, instance):
        return str(instance.fiscal_year)

    def get_dates(self, instance):
        return instance.dates

    def get_metadata(self, instance):
        return instance.metadata

    def get_last_modified(self, instance):
        # format_str = '%Y-%m-%d %Z'
        my_str = ""
        if instance.updated_at:

            my_str += f"{naturaltime(instance.updated_at)}"
            if instance.modified_by:
                my_str += f" by {instance.modified_by}"
        return my_str

    def get_deliverables_html(self, instance):
        return instance.deliverables_html

    def get_priorities_html(self, instance):
        return instance.priorities_html

    def get_technical_service_needs_html(self, instance):
        return markdown(instance.technical_service_needs) if instance.technical_service_needs else None

    def get_mobilization_needs_html(self, instance):
        return markdown(instance.mobilization_needs) if instance.mobilization_needs else None

    def get_vehicle_needs_html(self, instance):
        return markdown(instance.vehicle_needs) if instance.vehicle_needs else None

    def get_ship_needs_html(self, instance):
        return markdown(instance.ship_needs) if instance.ship_needs else None

    def get_instrumentation_html(self, instance):
        return markdown(instance.instrumentation) if instance.instrumentation else None

    def get_data_collected_html(self, instance):
        return markdown(instance.data_collected) if instance.data_collected else None

    def get_data_products_html(self, instance):
        return markdown(instance.data_products) if instance.data_products else None

    def get_data_storage_plan_html(self, instance):
        return markdown(instance.data_storage_plan) if instance.data_storage_plan else None

    def get_data_management_needs_html(self, instance):
        return markdown(instance.data_management_needs) if instance.data_management_needs else None

    def get_other_lab_support_needs_html(self, instance):
        return markdown(instance.other_lab_support_needs) if instance.other_lab_support_needs else None

    def get_it_needs_html(self, instance):
        return markdown(instance.it_needs) if instance.it_needs else None

    def get_field_staff_needs_html(self, instance):
        return markdown(instance.field_staff_needs) if instance.field_staff_needs else None

    def get_can_modify(self, instance):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return can_modify_project(user, instance.project_id)

    def get_submitted(self, instance):
        if instance.submitted:
            return instance.submitted.strftime("%Y-%m-%d")

    def get_default_funding_source_id(self, instance):
        return instance.project.default_funding_source_id

    def get_formatted_status(self, instance):
        return instance.formatted_status


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Staff
        fields = "__all__"

    smart_name = serializers.SerializerMethodField()
    employee_type_display = serializers.SerializerMethodField()
    level_display = serializers.SerializerMethodField()
    funding_source_display = serializers.SerializerMethodField()
    student_program_display = serializers.SerializerMethodField()
    project_year_obj = serializers.SerializerMethodField()

    def get_project_year_obj(self, instance):
        return ProjectYearSerializerLITE(instance.project_year).data

    def get_smart_name(self, instance):
        return instance.smart_name

    def get_employee_type_display(self, instance):
        return str(instance.employee_type) if instance.employee_type else None

    def get_level_display(self, instance):
        return str(instance.level) if instance.level else None

    def get_funding_source_display(self, instance):
        return str(instance.funding_source) if instance.funding_source else None

    def get_student_program_display(self, instance):
        return instance.get_student_program_display()


class OMCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OMCost
        fields = "__all__"

    funding_source_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    project_year_id = serializers.SerializerMethodField()
    category_type = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()

    def get_project_id(self, instance):
        return instance.project_year.project_id

    def get_funding_source_display(self, instance):
        return str(instance.funding_source)

    def get_category_display(self, instance):
        return instance.om_category.tname

    def get_project_year_id(self, instance):
        return instance.project_year_id

    def get_category_type(self, instance):
        return instance.category_type


class CapitalCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CapitalCost
        fields = "__all__"

    funding_source_display = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    project_year_id = serializers.SerializerMethodField()

    def get_funding_source_display(self, instance):
        return str(instance.funding_source)

    def get_category_display(self, instance):
        return str(instance.get_category_display())

    def get_project_year_id(self, instance):
        return instance.project_year_id


class AllocationSerializer(serializers.ModelSerializer):
    funding_source_display = serializers.SerializerMethodField()
    project_year_id = serializers.SerializerMethodField()
    distributed_amount = serializers.SerializerMethodField()

    def get_funding_source_display(self, instance):
        return str(instance.funding_source)

    def get_project_year_id(self, instance):
        return instance.project_year_id

    def get_distributed_amount(self, instance):
        return instance.distributed_amount

class SalaryAllocationSerializer(AllocationSerializer):
    class Meta:
        model = models.SalaryAllocation
        fields = "__all__"


class OMAllocationSerializer(AllocationSerializer):
    class Meta:
        model = models.OMAllocation
        fields = "__all__"


class CapitalAllocationSerializer(AllocationSerializer):
    class Meta:
        model = models.CapitalAllocation
        fields = "__all__"


class ActivitySerializer(serializers.ModelSerializer):
    target_date = serializers.DateField(format=None, input_formats=None, required=False, allow_null=True)
    target_start_date = serializers.DateField(format=None, input_formats=None, required=False, allow_null=True)

    class Meta:
        model = models.Activity
        fields = "__all__"

    latest_update = serializers.SerializerMethodField()
    target_date_display = serializers.SerializerMethodField()
    project_year_id = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()
    risk_rating_display = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()
    responsible_parties_display = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    latest_update_text = serializers.SerializerMethodField()
    latest_update_status = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_children(self, instance):
        if instance.children.exists():
            return [ActivitySerializer(obj).data for obj in instance.children.all()]
        return list()

    def get_duration(self, instance):
        if instance.target_start_date and instance.target_date:
            return (instance.target_date - instance.target_start_date).total_seconds() * 1000
        # otherwise return just a single day
        return 7 * 24 * 60 * 60 * 1000

    def get_responsible_parties_display(self, instance):
        if instance.responsible_parties.exists():
            return listrify(instance.responsible_parties.all())

    def get_dates(self, instance):
        return instance.dates

    def get_type_display(self, instance):
        return instance.get_type_display()

    def get_risk_rating_display(self, instance):
        return instance.get_risk_rating_display()

    def get_latest_update(self, instance):
        if instance.latest_update:
            return f'<a target="_blank" href="{reverse("ppt:report_detail", args=[instance.latest_update.status_report.id])}">{instance.latest_update.get_status_display()}</a>'
        return "n/a"

    def get_latest_update_text(self, instance):
        if instance.latest_update:
            return f'{instance.latest_update.get_status_display()}'
        return "n/a"

    def get_latest_update_status(self, instance):
        if instance.latest_update:
            return instance.latest_update.status

    def get_target_date_display(self, instance):
        if instance.target_date:
            return instance.target_date.strftime("%Y-%m-%d")

    def get_project_year_id(self, instance):
        return instance.project_year_id

    def validate(self, attrs):
        """
        form validation:
        - make that there is at least a project, project year or status report
        """
        target_date = attrs.get("target_date")
        target_start_date = attrs.get("target_start_date")

        if target_date and target_start_date and target_start_date > target_date:
            msg = _('The target end date must occur after the target start date.')
            raise ValidationError(msg)
        return attrs


class CollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collaboration
        fields = "__all__"

    project_year_id = serializers.SerializerMethodField()
    new_or_existing_display = serializers.SerializerMethodField()
    type_display = serializers.SerializerMethodField()

    def get_type_display(self, instance):
        return instance.get_type_display()

    def get_new_or_existing_display(self, instance):
        return instance.get_new_or_existing_display()

    def get_project_year_id(self, instance):
        return instance.project_year_id


class StatusReportSerializer(serializers.ModelSerializer):
    target_completion_date = serializers.DateField(format=None, input_formats=None, required=False, allow_null=True)

    class Meta:
        model = models.StatusReport
        fields = "__all__"

    target_completion_date_display = serializers.SerializerMethodField()
    report_number = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    supporting_resources = serializers.SerializerMethodField()
    major_accomplishments_html = serializers.SerializerMethodField()
    major_issues_html = serializers.SerializerMethodField()

    def get_major_accomplishments_html(self, instance):
        return instance.major_accomplishments_html

    def get_major_issues_html(self, instance):
        return instance.major_issues_html

    def get_target_completion_date_display(self, instance):
        if instance.target_completion_date:
            return instance.target_completion_date.strftime("%Y-%m-%d")

    def get_report_number(self, instance):
        return instance.report_number

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_supporting_resources(self, instance):
        return instance.files.count()


class ActivityUpdateSerializer(serializers.ModelSerializer):
    activity = serializers.StringRelatedField()
    status_display = serializers.SerializerMethodField()
    notes_html = serializers.SerializerMethodField()
    metadata = serializers.SerializerMethodField()

    class Meta:
        model = models.ActivityUpdate
        exclude = ["status_report"]

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_notes_html(self, instance):
        return instance.notes_html

    def get_metadata(self, instance):
        return instance.metadata


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = "__all__"

    date_created = serializers.SerializerMethodField()
    ref = serializers.SerializerMethodField()

    def get_new_or_existing_display(self, instance):
        return instance.get_new_or_existing_display()

    def get_date_created(self, instance):
        return date(instance.date_created)

    def get_ref(self, instance):
        return instance.ref

    def validate(self, attrs):
        """
        form validation:
        - make that there is at least a project, project year or status report
        """
        project = attrs.get("project")
        project_year = attrs.get("project_year")
        status_report = attrs.get("status_report")
        file = attrs.get("file")

        if not (file or project or project_year or status_report):
            msg = _('You must supply either a project, project year or status report')
            raise ValidationError(msg)
        return attrs


class FiscalYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = shared_models.FiscalYear
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Theme
        fields = "__all__"


class FunctionalGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FunctionalGroup
        fields = "__all__"


class FundingSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FundingSource
        fields = "__all__"

    display = serializers.SerializerMethodField()

    def get_display(self, instance):
        return instance.display2


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = shared_models.Region
        fields = "__all__"


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = shared_models.Division
        fields = "__all__"

    display = serializers.SerializerMethodField()

    def get_display(self, instance):
        return str(instance)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = shared_models.Section
        fields = "__all__"

    full_name = serializers.SerializerMethodField()

    def get_full_name(self, instance):
        return instance.full_name


class CitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = shared_models.Citation
        fields = "__all__"

    short_citation_html = serializers.SerializerMethodField()
    citation_br = serializers.SerializerMethodField()
    turl = serializers.SerializerMethodField()
    tname = serializers.SerializerMethodField()
    tabstract = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()

    def get_project_count(self, instance):
        return instance.projects.count()

    def get_tabstract(self, instance):
        return instance.tabstract

    def get_tname(self, instance):
        return instance.tname

    def get_turl(self, instance):
        return instance.turl

    def get_citation_br(self, instance):
        return instance.citation_br

    def get_short_citation_html(self, instance):
        return instance.short_citation_html


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = shared_models.Publication
        fields = "__all__"


class DMASerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DMA
        fields = "__all__"

    metadata = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    region_display = serializers.SerializerMethodField()
    section_display = serializers.SerializerMethodField()

    def get_section_display(self, instance):
        return str(instance.project.section)

    def get_region_display(self, instance):
        return str(instance.project.section.division.branch.sector.region)

    def get_status_display(self, instance):
        return instance.get_status_display()

    def get_metadata(self, instance):
        return instance.metadata
