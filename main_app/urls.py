"""
URL configuration for main_app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views.product_info import ProductInfoView
from .views.login import LoginView
from .views.logout import Logout
from .views.register import RegisterRequestView, RegisterDoneView, RegisterCompleteView, RegisterErrorView
from .views.password_forgot  import PasswordForgotView, PasswordForgotDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views.top import TopView
from .views.user_settings import UserSettingsView
from .views.password_change import PasswordChangeView, PasswordChangeDoneView

from .views.dev.charts import ChartsApexChartsView, ChartsChartjsView, ChartsEchartsView
from .views.dev.components import ComponentsAccordionView, ComponentsAlertsView, ComponentsBadgesView, ComponentsBreadcrumbsView, ComponentsButtonsView, ComponentsCardsView, ComponentsCarouselView, ComponentsListGroupView, ComponentsModalView, ComponentsPaginationView, ComponentsProgressView, ComponentsSpinnersView, ComponentsTabsView, ComponentsTooltipsView
from .views.dev.forms import FormsEditors, FormsElements, FormsLayouts, FormsValidation
from .views.dev.icons import IconsBootstrap, IconsBoxicons, IconsRemix
from .views.dev.pages import Dashboard, PagesBlank, PagesContact, PagesError404, PagesFAQ, PagesLogin, PagesRegister, UsersProfile
from .views.dev.tables import TablesData, TablesGeneral
from .views.reservation import ReservationView, ReservationDoneView

app_name = 'main_app'

urlpatterns = [
    path("", ProductInfoView.as_view(), name="product_info" ),

    path("login/" , LoginView.as_view(), name="login" ),
    path("logout/", Logout.as_view()   , name="logout"),

    path("register/"                             , RegisterRequestView.as_view() , name="register_request" ),
    path("register/done/<uuid:user_id>/"         , RegisterDoneView.as_view()    , name="register_done"    ),
    path('register/check/<uuid:activate_token>/' , RegisterCompleteView.as_view(), name='register_complete'),
    path('register/check/error/<int:error_code>/', RegisterErrorView.as_view()   , name='register_error'   ),

    # forgot-password
    path('password/forgot/'                        , PasswordForgotView.as_view()       , name='password_forgot'        ),
    path('password/forgot/done/'                   , PasswordForgotDoneView.as_view()   , name='password_forgot_done'   ),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view() , name='password_reset_confirm' ),
    path('password/reset/complete/'                , PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path("top/", TopView.as_view(), name="top"),

    path("settings/", UserSettingsView.as_view(), name="user_settings"),

    path("settings/password/change/"     , PasswordChangeView.as_view()    , name="password_change"     ),
    path("settings/password/change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),

    path("reservation/"     , ReservationView.as_view()    , name="reservation"     ),
    path("reservation/done/", ReservationDoneView.as_view(), name="reservation_done"),

    # Developer Contents
    ## Charts
    path("dev/charts/apexcharts/", ChartsApexChartsView.as_view(), name="dev_charts_apexcharts"),
    path("dev/charts/chartjs/"   , ChartsChartjsView.as_view()   , name="dev_charts_chartjs"   ),
    path("dev/charts/echarts/"   , ChartsEchartsView.as_view()   , name="dev_charts_echarts"   ),

    ## Components
    path("dev/components/accordion/"  , ComponentsAccordionView.as_view()  , name="dev_components_accordion"  ),
    path("dev/components/alerts/"     , ComponentsAlertsView.as_view()     , name="dev_components_alerts"     ),
    path("dev/components/badges/"     , ComponentsBadgesView.as_view()     , name="dev_components_badges"     ),
    path("dev/components/breadcrumbs/", ComponentsBreadcrumbsView.as_view(), name="dev_components_breadcrumbs"),
    path("dev/components/buttons/"    , ComponentsButtonsView.as_view()    , name="dev_components_buttons"    ),
    path("dev/components/cards/"      , ComponentsCardsView.as_view()      , name="dev_components_cards"      ),
    path("dev/components/carousel/"   , ComponentsCarouselView.as_view()   , name="dev_components_carousel"   ),
    path("dev/components/list-group/" , ComponentsListGroupView.as_view()  , name="dev_components_list_group" ),
    path("dev/components/modal/"      , ComponentsModalView.as_view()      , name="dev_components_modal"      ),
    path("dev/components/pagination/" , ComponentsPaginationView.as_view() , name="dev_components_pagination" ),
    path("dev/components/progress/"   , ComponentsProgressView.as_view()   , name="dev_components_progress"   ),
    path("dev/components/spinners/"   , ComponentsSpinnersView.as_view()   , name="dev_components_spinners"   ),
    path("dev/components/tabs/"       , ComponentsTabsView.as_view()       , name="dev_components_tabs"       ),
    path("dev/components/tooltips/"   , ComponentsTooltipsView.as_view()   , name="dev_components_tooltips"   ),

    ## Forms
    path("dev/forms/editors/"   , FormsEditors.as_view()   , name="dev_forms_editors"   ),
    path("dev/forms/elements/"  , FormsElements.as_view()  , name="dev_forms_elements"  ),
    path("dev/forms/layouts/"   , FormsLayouts.as_view()   , name="dev_forms_layouts"   ),
    path("dev/forms/validation/", FormsValidation.as_view(), name="dev_forms_validation"),

    ## Icons
    path("dev/icons/bootstrap/", IconsBootstrap.as_view(), name="dev_icons_bootstrap"),
    path("dev/icons/boxicons/" , IconsBoxicons.as_view() , name="dev_icons_boxicons" ),
    path("dev/icons/remix/"    , IconsRemix.as_view()    , name="dev_icons_remix"    ),

    ## Pages
    path("dev/pages/dashboard/"    , Dashboard.as_view()    , name="dev_pages_dashboard"    ),
    path("dev/pages/blank/"        , PagesBlank.as_view()   , name="dev_pages_blank"        ),
    path("dev/pages/contact/"      , PagesContact.as_view() , name="dev_pages_contact"      ),
    path("dev/pages/error-404/"    , PagesError404.as_view(), name="dev_pages_error_404"    ),
    path("dev/pages/faq/"          , PagesFAQ.as_view()     , name="dev_pages_faq"          ),
    path("dev/pages/login/"        , PagesLogin.as_view()   , name="dev_pages_login"        ),
    path("dev/pages/register/"     , PagesRegister.as_view(), name="dev_pages_register"     ),
    path("dev/pages/users-profile/", UsersProfile.as_view() , name="dev_pages_users_profile"),

    ## Tables
    path("dev/tables/data/"   , TablesData.as_view()   , name="dev_tables_data"   ),
    path("dev/tables/general/", TablesGeneral.as_view(), name="dev_tables_general"),


]