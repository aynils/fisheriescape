from django.urls import path
from . import views

app_name = 'bio_diversity'

urlpatterns = [
    # for home/index page
    path('', views.IndexTemplateView.as_view(),    name="index"),

    path('create/anidc/', views.AnidcCreate.as_view(), name="create_anidc"),
    path('details/anidc/<int:pk>/', views.AnidcDetails.as_view(), name="details_anidc"),
    path('list/anidc/', views.AnidcList.as_view(), name="list_anidc"),
    path('update/anidc/<int:pk>/', views.AnidcUpdate.as_view(), name="update_anidc"),
    
    path('create/adsc/', views.AdscCreate.as_view(), name="create_adsc"),
    path('details/adsc/<int:pk>/', views.AdscDetails.as_view(), name="details_adsc"),
    path('list/adsc/', views.AdscList.as_view(), name="list_adsc"),
    path('update/adsc/<int:pk>/', views.AdscUpdate.as_view(), name="update_adsc"),
    
    path('create/cnt/', views.CntCreate.as_view(), name="create_cnt"),
    path('details/cnt/<int:pk>/', views.CntDetails.as_view(), name="details_cnt"),
    path('list/cnt/', views.CntList.as_view(), name="list_cnt"),
    path('update/cnt/<int:pk>/', views.CntUpdate.as_view(), name="update_cnt"),
    
    path('create/cntc/', views.CntcCreate.as_view(), name="create_cntc"),
    path('details/cntc/<int:pk>/', views.CntcDetails.as_view(), name="details_cntc"),
    path('list/cntc/', views.CntcList.as_view(), name="list_cntc"),
    path('update/cntc/<int:pk>/', views.CntcUpdate.as_view(), name="update_cntc"),
    
    path('create/cntd/', views.CntdCreate.as_view(), name="create_cntd"),
    path('details/cntd/<int:pk>/', views.CntdDetails.as_view(), name="details_cntd"),
    path('list/cntd/', views.CntdList.as_view(), name="list_cntd"),
    path('update/cntd/<int:pk>/', views.CntdUpdate.as_view(), name="update_cntd"),
    
    path('create/coll/', views.CollCreate.as_view(), name="create_coll"),
    path('details/coll/<int:pk>/', views.CollDetails.as_view(), name="details_coll"),
    path('list/coll/', views.CollList.as_view(), name="list_coll"),
    path('update/coll/<int:pk>/', views.CollUpdate.as_view(), name="update_coll"),

    path('create/contdc/', views.ContdcCreate.as_view(), name="create_contdc"),
    path('details/contdc/<int:pk>/', views.ContdcDetails.as_view(), name="details_contdc"),
    path('list/contdc/', views.ContdcList.as_view(), name="list_contdc"),
    path('update/contdc/<int:pk>/', views.ContdcUpdate.as_view(), name="update_contdc"),

    path('create/contx/', views.ContxCreate.as_view(), name="create_contx"),
    path('details/contx/<int:pk>/', views.ContxDetails.as_view(), name="details_contx"),
    path('list/contx/', views.ContxList.as_view(), name="list_contx"),
    path('update/contx/<int:pk>/', views.ContxUpdate.as_view(), name="update_contx"),

    path('create/cdsc/', views.CdscCreate.as_view(), name="create_cdsc"),
    path('details/cdsc/<int:pk>/', views.CdscDetails.as_view(), name="details_cdsc"),
    path('list/cdsc/', views.CdscList.as_view(), name="list_cdsc"),
    path('update/cdsc/<int:pk>/', views.CdscUpdate.as_view(), name="update_cdsc"),

    path('create/cup/', views.CupCreate.as_view(), name="create_cup"),
    path('details/cup/<int:pk>/', views.CupDetails.as_view(), name="details_cup"),
    path('list/cup/', views.CupList.as_view(), name="list_cup"),
    path('update/cup/<int:pk>/', views.CupUpdate.as_view(), name="update_cup"),
    
    path('create/cupd/', views.CupdCreate.as_view(), name="create_cupd"),
    path('details/cupd/<int:pk>/', views.CupdDetails.as_view(), name="details_cupd"),
    path('list/cupd/', views.CupdList.as_view(), name="list_cupd"),
    path('update/cupd/<int:pk>/', views.CupdUpdate.as_view(), name="update_cupd"),
        
    path('create/draw/', views.DrawCreate.as_view(), name="create_draw"),
    path('details/draw/<int:pk>/', views.DrawDetails.as_view(), name="details_draw"),
    path('list/draw/', views.DrawList.as_view(), name="list_draw"),
    path('update/draw/<int:pk>/', views.DrawUpdate.as_view(), name="update_draw"),
        
    path('create/env/', views.EnvCreate.as_view(), name="create_env"),
    path('details/env/<int:pk>/', views.EnvDetails.as_view(), name="details_env"),
    path('list/env/', views.EnvList.as_view(), name="list_env"),
    path('update/env/<int:pk>/', views.EnvUpdate.as_view(), name="update_env"),   
    
    path('create/envc/', views.EnvcCreate.as_view(), name="create_envc"),
    path('details/envc/<int:pk>/', views.EnvcDetails.as_view(), name="details_envc"),
    path('list/envc/', views.EnvcList.as_view(), name="list_envc"),
    path('update/envc/<int:pk>/', views.EnvcUpdate.as_view(), name="update_envc"),   
    
    path('create/envsc/', views.EnvscCreate.as_view(), name="create_envsc"),
    path('details/envsc/<int:pk>/', views.EnvscDetails.as_view(), name="details_envsc"),
    path('list/envsc/', views.EnvscList.as_view(), name="list_envsc"),
    path('update/envsc/<int:pk>/', views.EnvscUpdate.as_view(), name="update_envsc"),  
    
    path('create/envt/', views.EnvtCreate.as_view(), name="create_envt"),
    path('details/envt/<int:pk>/', views.EnvtDetails.as_view(), name="details_envt"),
    path('list/envt/', views.EnvtList.as_view(), name="list_envt"),
    path('update/envt/<int:pk>/', views.EnvtUpdate.as_view(), name="update_envt"),  
    
    path('create/envtc/', views.EnvtcCreate.as_view(), name="create_envtc"),
    path('details/envtc/<int:pk>/', views.EnvtcDetails.as_view(), name="details_envtc"),
    path('list/envtc/', views.EnvtcList.as_view(), name="list_envtc"),
    path('update/envtc/<int:pk>/', views.EnvtcUpdate.as_view(), name="update_envtc"),  
    
    path('create/evnt/', views.EvntCreate.as_view(), name="create_evnt"),
    path('details/evnt/<int:pk>/', views.EvntDetails.as_view(), name="details_evnt"),
    path('list/evnt/', views.EvntList.as_view(), name="list_evnt"),
    path('update/evnt/<int:pk>/', views.EvntUpdate.as_view(), name="update_evnt"),
                  
    path('create/evntc/', views.EvntcCreate.as_view(), name="create_evntc"),
    path('details/evntc/<int:pk>/', views.EvntcDetails.as_view(), name="details_evntc"),
    path('list/evntc/', views.EvntcList.as_view(), name="list_evntc"),
    path('update/evntc/<int:pk>/', views.EvntcUpdate.as_view(), name="update_evntc"),
            
    path('create/facic/', views.FacicCreate.as_view(), name="create_facic"),
    path('details/facic/<int:pk>/', views.FacicDetails.as_view(), name="details_facic"),
    path('list/facic/', views.FacicList.as_view(), name="list_facic"),
    path('update/facic/<int:pk>/', views.FacicUpdate.as_view(), name="update_facic"),
                         
    path('create/fecu/', views.FecuCreate.as_view(), name="create_fecu"),
    path('details/fecu/<int:pk>/', views.FecuDetails.as_view(), name="details_fecu"),
    path('list/fecu/', views.FecuList.as_view(), name="list_fecu"),
    path('update/fecu/<int:pk>/', views.FecuUpdate.as_view(), name="update_fecu"),
             
    path('create/feed/', views.FeedCreate.as_view(), name="create_feed"),
    path('details/feed/<int:pk>/', views.FeedDetails.as_view(), name="details_feed"),
    path('list/feed/', views.FeedList.as_view(), name="list_feed"),
    path('update/feed/<int:pk>/', views.FeedUpdate.as_view(), name="update_feed"),
             
    path('create/feedc/', views.FeedcCreate.as_view(), name="create_feedc"),
    path('details/feedc/<int:pk>/', views.FeedcDetails.as_view(), name="details_feedc"),
    path('list/feedc/', views.FeedcList.as_view(), name="list_feedc"),
    path('update/feedc/<int:pk>/', views.FeedcUpdate.as_view(), name="update_feedc"),
             
    path('create/feedm/', views.FeedmCreate.as_view(), name="create_feedm"),
    path('details/feedm/<int:pk>/', views.FeedmDetails.as_view(), name="details_feedm"),
    path('list/feedm/', views.FeedmList.as_view(), name="list_feedm"),
    path('update/feedm/<int:pk>/', views.FeedmUpdate.as_view(), name="update_feedm"),
                 
    path('create/grp/', views.GrpCreate.as_view(), name="create_grp"),
    path('details/grp/<int:pk>/', views.GrpDetails.as_view(), name="details_grp"),
    path('list/grp/', views.GrpList.as_view(), name="list_grp"),
    path('update/grp/<int:pk>/', views.GrpUpdate.as_view(), name="update_grp"),
    
    path('create/heat/', views.HeatCreate.as_view(), name="create_heat"),
    path('details/heat/<int:pk>/', views.HeatDetails.as_view(), name="details_heat"),
    path('list/heat/', views.HeatList.as_view(), name="list_heat"),
    path('update/heat/<int:pk>/', views.HeatUpdate.as_view(), name="update_heat"),
    
    path('create/heatd/', views.HeatdCreate.as_view(), name="create_heatd"),
    path('details/heatd/<int:pk>/', views.HeatdDetails.as_view(), name="details_heatd"),
    path('list/heatd/', views.HeatdList.as_view(), name="list_heatd"),
    path('update/heatd/<int:pk>/', views.HeatdUpdate.as_view(), name="update_heatd"),

    path('create/indv/', views.IndvCreate.as_view(), name="create_indv"),
    path('details/indv/<int:pk>/', views.IndvDetails.as_view(), name="details_indv"),
    path('list/indv/', views.IndvList.as_view(), name="list_indv"),
    path('update/indv/<int:pk>/', views.IndvUpdate.as_view(), name="update_indv"),

    path('create/indvt/', views.IndvtCreate.as_view(), name="create_indvt"),
    path('details/indvt/<int:pk>/', views.IndvtDetails.as_view(), name="details_indvt"),
    path('list/indvt/', views.IndvtList.as_view(), name="list_indvt"),
    path('update/indvt/<int:pk>/', views.IndvtUpdate.as_view(), name="update_indvt"),

    path('create/indvtc/', views.IndvtcCreate.as_view(), name="create_indvtc"),
    path('details/indvtc/<int:pk>/', views.IndvtcDetails.as_view(), name="details_indvtc"),
    path('list/indvtc/', views.IndvtcList.as_view(), name="list_indvtc"),
    path('update/indvtc/<int:pk>/', views.IndvtcUpdate.as_view(), name="update_indvtc"),

    path('create/inst/', views.InstCreate.as_view(), name="create_inst"),
    path('details/inst/<int:pk>/', views.InstDetails.as_view(), name="details_inst"),
    path('list/inst/', views.InstList.as_view(), name="list_inst"),
    path('update/inst/<int:pk>/', views.InstUpdate.as_view(), name="update_inst"),

    path('create/instc/', views.InstcCreate.as_view(), name="create_instc"),
    path('details/instc/<int:pk>/', views.InstcDetails.as_view(), name="details_instc"),
    path('list/instc/', views.InstcList.as_view(), name="list_instc"),
    path('update/instc/<int:pk>/', views.InstcUpdate.as_view(), name="update_instc"),

    path('create/instd/', views.InstdCreate.as_view(), name="create_instd"),
    path('details/instd/<int:pk>/', views.InstdDetails.as_view(), name="details_instd"),
    path('list/instd/', views.InstdList.as_view(), name="list_instd"),
    path('update/instd/<int:pk>/', views.InstdUpdate.as_view(), name="update_instd"),

    path('create/instdc/', views.InstdcCreate.as_view(), name="create_instdc"),
    path('details/instdc/<int:pk>/', views.InstdcDetails.as_view(), name="details_instdc"),
    path('list/instdc/', views.InstdcList.as_view(), name="list_instdc"),
    path('update/instdc/<int:pk>/', views.InstdcUpdate.as_view(), name="update_instdc"),

    path('create/loc/', views.LocCreate.as_view(), name="create_loc"),
    path('details/loc/<int:pk>/', views.LocDetails.as_view(), name="details_loc"),
    path('list/loc/', views.LocList.as_view(), name="list_loc"),
    path('update/loc/<int:pk>/', views.LocUpdate.as_view(), name="update_loc"),

    path('create/locc/', views.LoccCreate.as_view(), name="create_locc"),
    path('details/locc/<int:pk>/', views.LoccDetails.as_view(), name="details_locc"),
    path('list/locc/', views.LoccList.as_view(), name="list_locc"),
    path('update/locc/<int:pk>/', views.LoccUpdate.as_view(), name="update_locc"),

    path('create/orga/', views.OrgaCreate.as_view(), name="create_orga"),
    path('details/orga/<int:pk>/', views.OrgaDetails.as_view(), name="details_orga"),
    path('list/orga/', views.OrgaList.as_view(), name="list_orga"),
    path('update/orga/<int:pk>/', views.OrgaUpdate.as_view(), name="update_orga"),

    path('create/pair/', views.PairCreate.as_view(), name="create_pair"),
    path('details/pair/<int:pk>/', views.PairDetails.as_view(), name="details_pair"),
    path('list/pair/', views.PairList.as_view(), name="list_pair"),
    path('update/pair/<int:pk>/', views.PairUpdate.as_view(), name="update_pair"),

    path('create/perc/', views.PercCreate.as_view(), name="create_perc"),
    path('details/perc/<int:pk>/', views.PercDetails.as_view(), name="details_perc"),
    path('list/perc/', views.PercList.as_view(), name="list_perc"),
    path('update/perc/<int:pk>/', views.PercUpdate.as_view(), name="update_perc"),

    path('create/prio/', views.PrioCreate.as_view(), name="create_prio"),
    path('details/prio/<int:pk>/', views.PrioDetails.as_view(), name="details_prio"),
    path('list/prio/', views.PrioList.as_view(), name="list_prio"),
    path('update/prio/<int:pk>/', views.PrioUpdate.as_view(), name="update_prio"),

    path('create/prog/', views.ProgCreate.as_view(), name="create_prog"),
    path('details/prog/<int:pk>/', views.ProgDetails.as_view(), name="details_prog"),
    path('list/prog/', views.ProgList.as_view(), name="list_prog"),
    path('update/prog/<int:pk>/', views.ProgUpdate.as_view(), name="update_prog"),

    path('create/proga/', views.ProgaCreate.as_view(), name="create_proga"),
    path('details/proga/<int:pk>/', views.ProgaDetails.as_view(), name="details_proga"),
    path('list/proga/', views.ProgaList.as_view(), name="list_proga"),
    path('update/proga/<int:pk>/', views.ProgaUpdate.as_view(), name="update_proga"),

    path('create/prot/', views.ProtCreate.as_view(), name="create_prot"),
    path('details/prot/<int:pk>/', views.ProtDetails.as_view(), name="details_prot"),
    path('list/prot/', views.ProtList.as_view(), name="list_prot"),
    path('update/prot/<int:pk>/', views.ProtUpdate.as_view(), name="update_prot"),

    path('create/protc/', views.ProtcCreate.as_view(), name="create_protc"),
    path('details/protc/<int:pk>/', views.ProtcDetails.as_view(), name="details_protc"),
    path('list/protc/', views.ProtcList.as_view(), name="list_protc"),
    path('update/protc/<int:pk>/', views.ProtcUpdate.as_view(), name="update_protc"),

    path('create/protf/', views.ProtfCreate.as_view(), name="create_protf"),
    path('details/protf/<int:pk>/', views.ProtfDetails.as_view(), name="details_protf"),
    path('list/protf/', views.ProtfList.as_view(), name="list_protf"),
    path('update/protf/<int:pk>/', views.ProtfUpdate.as_view(), name="update_protf"),

    path('create/qual/', views.QualCreate.as_view(), name="create_qual"),
    path('details/qual/<int:pk>/', views.QualDetails.as_view(), name="details_qual"),
    path('list/qual/', views.QualList.as_view(), name="list_qual"),
    path('update/qual/<int:pk>/', views.QualUpdate.as_view(), name="update_qual"),

    path('create/relc/', views.RelcCreate.as_view(), name="create_relc"),
    path('details/relc/<int:pk>/', views.RelcDetails.as_view(), name="details_relc"),
    path('list/relc/', views.RelcList.as_view(), name="list_relc"),
    path('update/relc/<int:pk>/', views.RelcUpdate.as_view(), name="update_relc"),
    
    path('create/rive/', views.RiveCreate.as_view(), name="create_rive"),
    path('details/rive/<int:pk>/', views.RiveDetails.as_view(), name="details_rive"),
    path('list/rive/', views.RiveList.as_view(), name="list_rive"),
    path('update/rive/<int:pk>/', views.RiveUpdate.as_view(), name="update_rive"),
    
    path('create/role/', views.RoleCreate.as_view(), name="create_role"),
    path('details/role/<int:pk>/', views.RoleDetails.as_view(), name="details_role"),
    path('list/role/', views.RoleList.as_view(), name="list_role"),
    path('update/role/<int:pk>/', views.RoleUpdate.as_view(), name="update_role"),

    path('create/samp/', views.SampCreate.as_view(), name="create_samp"),
    path('details/samp/<int:pk>/', views.SampDetails.as_view(), name="details_samp"),
    path('list/samp/', views.SampList.as_view(), name="list_samp"),
    path('update/samp/<int:pk>/', views.SampUpdate.as_view(), name="update_samp"),

    path('create/sampc/', views.SampcCreate.as_view(), name="create_sampc"),
    path('details/sampc/<int:pk>/', views.SampcDetails.as_view(), name="details_sampc"),
    path('list/sampc/', views.SampcList.as_view(), name="list_sampc"),
    path('update/sampc/<int:pk>/', views.SampcUpdate.as_view(), name="update_sampc"),

    path('create/sampd/', views.SampdCreate.as_view(), name="create_sampd"),
    path('details/sampd/<int:pk>/', views.SampdDetails.as_view(), name="details_sampd"),
    path('list/sampd/', views.SampdList.as_view(), name="list_sampd"),
    path('update/sampd/<int:pk>/', views.SampdUpdate.as_view(), name="update_sampd"),

    path('create/sire/', views.SireCreate.as_view(), name="create_sire"),
    path('details/sire/<int:pk>/', views.SireDetails.as_view(), name="details_sire"),
    path('list/sire/', views.SireList.as_view(), name="list_sire"),
    path('update/sire/<int:pk>/', views.SireUpdate.as_view(), name="update_sire"),

    path('create/spwn/', views.SpwnCreate.as_view(), name="create_spwn"),
    path('details/spwn/<int:pk>/', views.SpwnDetails.as_view(), name="details_spwn"),
    path('list/spwn/', views.SpwnList.as_view(), name="list_spwn"),
    path('update/spwn/<int:pk>/', views.SpwnUpdate.as_view(), name="update_spwn"),
    
    path('create/spwnd/', views.SpwndCreate.as_view(), name="create_spwnd"),
    path('details/spwnd/<int:pk>/', views.SpwndDetails.as_view(), name="details_spwnd"),
    path('list/spwnd/', views.SpwndList.as_view(), name="list_spwnd"),
    path('update/spwnd/<int:pk>/', views.SpwndUpdate.as_view(), name="update_spwnd"),
    
    path('create/spwndc/', views.SpwndcCreate.as_view(), name="create_spwndc"),
    path('details/spwndc/<int:pk>/', views.SpwndcDetails.as_view(), name="details_spwndc"),
    path('list/spwndc/', views.SpwndcList.as_view(), name="list_spwndc"),
    path('update/spwndc/<int:pk>/', views.SpwndcUpdate.as_view(), name="update_spwndc"),
    
    path('create/spwnsc/', views.SpwnscCreate.as_view(), name="create_spwnsc"),
    path('details/spwnsc/<int:pk>/', views.SpwnscDetails.as_view(), name="details_spwnsc"),
    path('list/spwnsc/', views.SpwnscList.as_view(), name="list_spwnsc"),
    path('update/spwnsc/<int:pk>/', views.SpwnscUpdate.as_view(), name="update_spwnsc"),
    
    path('create/spec/', views.SpecCreate.as_view(), name="create_spec"),
    path('details/spec/<int:pk>/', views.SpecDetails.as_view(), name="details_spec"),
    path('list/spec/', views.SpecList.as_view(), name="list_spec"),
    path('update/spec/<int:pk>/', views.SpecUpdate.as_view(), name="update_spec"),
    
    path('create/stok/', views.StokCreate.as_view(), name="create_stok"),
    path('details/stok/<int:pk>/', views.StokDetails.as_view(), name="details_stok"),
    path('list/stok/', views.StokList.as_view(), name="list_stok"),
    path('update/stok/<int:pk>/', views.StokUpdate.as_view(), name="update_stok"),
    
    path('create/subr/', views.SubrCreate.as_view(), name="create_subr"),
    path('details/subr/<int:pk>/', views.SubrDetails.as_view(), name="details_subr"),
    path('list/subr/', views.SubrList.as_view(), name="list_subr"),
    path('update/subr/<int:pk>/', views.SubrUpdate.as_view(), name="update_subr"),

    path('create/tank/', views.TankCreate.as_view(), name="create_tank"),
    path('details/tank/<int:pk>/', views.TankDetails.as_view(), name="details_tank"),
    path('list/tank/', views.TankList.as_view(), name="list_tank"),
    path('update/tank/<int:pk>/', views.TankUpdate.as_view(), name="update_tank"),

    path('create/tankd/', views.TankdCreate.as_view(), name="create_tankd"),
    path('details/tankd/<int:pk>/', views.TankdDetails.as_view(), name="details_tankd"),
    path('list/tankd/', views.TankdList.as_view(), name="list_tankd"),
    path('update/tankd/<int:pk>/', views.TankdUpdate.as_view(), name="update_tankd"),

    path('create/team/', views.TeamCreate.as_view(), name="create_team"),
    path('details/team/<int:pk>/', views.TeamDetails.as_view(), name="details_team"),
    path('list/team/', views.TeamList.as_view(), name="list_team"),
    path('update/team/<int:pk>/', views.TeamUpdate.as_view(), name="update_team"),

    path('create/tray/', views.TrayCreate.as_view(), name="create_tray"),
    path('details/tray/<int:pk>/', views.TrayDetails.as_view(), name="details_tray"),
    path('list/tray/', views.TrayList.as_view(), name="list_tray"),
    path('update/tray/<int:pk>/', views.TrayUpdate.as_view(), name="update_tray"),
    
    path('create/trayd/', views.TraydCreate.as_view(), name="create_trayd"),
    path('details/trayd/<int:pk>/', views.TraydDetails.as_view(), name="details_trayd"),
    path('list/trayd/', views.TraydList.as_view(), name="list_trayd"),
    path('update/trayd/<int:pk>/', views.TraydUpdate.as_view(), name="update_trayd"),
    
    path('create/trib/', views.TribCreate.as_view(), name="create_trib"),
    path('details/trib/<int:pk>/', views.TribDetails.as_view(), name="details_trib"),
    path('list/trib/', views.TribList.as_view(), name="list_trib"),
    path('update/trib/<int:pk>/', views.TribUpdate.as_view(), name="update_trib"),

    path('create/trof/', views.TrofCreate.as_view(), name="create_trof"),
    path('details/trof/<int:pk>/', views.TrofDetails.as_view(), name="details_trof"),
    path('list/trof/', views.TrofList.as_view(), name="list_trof"),
    path('update/trof/<int:pk>/', views.TrofUpdate.as_view(), name="update_trof"),
    
    path('create/trofd/', views.TrofdCreate.as_view(), name="create_trofd"),
    path('details/trofd/<int:pk>/', views.TrofdDetails.as_view(), name="details_trofd"),
    path('list/trofd/', views.TrofdList.as_view(), name="list_trofd"),
    path('update/trofd/<int:pk>/', views.TrofdUpdate.as_view(), name="update_trofd"),
    
    path('create/unit/', views.UnitCreate.as_view(), name="create_unit"),
    path('details/unit/<int:pk>/', views.UnitDetails.as_view(), name="details_unit"),
    path('list/unit/', views.UnitList.as_view(), name="list_unit"),
    path('update/unit/<int:pk>/', views.UnitUpdate.as_view(), name="update_unit"),

]
