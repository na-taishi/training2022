import datetime

from dateutil.relativedelta import relativedelta

from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm
from .forms import RouteForm
from .forms import ExpenseReportForm
from .models import Route
from .models import ExpenseReport


# Create your views here.
class LoginView(views.LoginView):
    '''ログイン'''
    template_name = "login.html"
    form_class = LoginForm


class LogoutView(LoginRequiredMixin,views.LogoutView):
    '''ログアウト'''
    template_name = "login.html"


class TopView(LoginRequiredMixin,generic.TemplateView):
    '''トップ
    ログイン後の遷移先
    '''
    template_name = "expense_report.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RouteView(LoginRequiredMixin,generic.FormView):
    '''経路'''
    template_name = "route_list.html"
    form_class = RouteForm
    success_url = reverse_lazy("webapp:route_list")

    def post(self, request, *args, **kwargs):
        # 更新処理時は初期値を入れる
        if request.POST['input_route_id'] == "0":
            route = None
        else:
            route = Route.objects.get(pk=request.POST['input_route_id'])
        form = self.form_class(request.POST, instance=route)
        if form.is_valid():
            route = form.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class RouteDeleteView(LoginRequiredMixin,generic.DeleteView):
    '''経路削除
    フォームで送信したroute_idに一致するデータを削除
    '''
    template_name = "route_list.html"
    model = Route
    success_url = reverse_lazy("webapp:route_list")

    def delete(self, request, *args, **kwargs):
        # 削除対象のpkを設定する
        self.kwargs['pk'] = request.POST['delete_route_id']
        return super().delete(request)


class RouteListView(LoginRequiredMixin,generic.ListView):
    '''経路一覧'''
    model = Route
    template_name = "route_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        route_dict = {}
        # ログイン中のアカウントを紐づける
        route_dict['account'] = self.request.user
        context['route_form'] = RouteForm(initial=route_dict)
        return context

    def get_queryset(self, **kwargs):
        account_id = self.request.user
        self.queryset = Route.objects.filter(account_id=account_id)
        queryset = super().get_queryset(**kwargs)
        return queryset


class ExpenseReportView(LoginRequiredMixin,generic.FormView):
    '''清算書'''
    template_name = "expense_report.html"
    form_class = ExpenseReportForm
    success_url = reverse_lazy("webapp:expense_report")
    dt = datetime.date.today()

    def set_date_range(self):
        '''期間範囲設定'''
        if "date" in self.request.GET:
            dt_time = datetime.datetime.strptime(self.request.GET['date'],'%Y年%m月%d日')
            # 時間部分を切り捨てる
            self.dt = datetime.date(dt_time.year,dt_time.month,dt_time.day)
            if "val" in self.request.GET:
                self.dt =  self.dt + relativedelta(months=int(self.request.GET['val']))
        elif "date" in self.request.POST:
            dt_time = datetime.datetime.strptime(self.request.POST['date'],'%Y年%m月%d日')
            self.dt = datetime.date(dt_time.year,dt_time.month,dt_time.day)
        self.dt_start = self.dt.replace(day=1)
        self.dt_end = self.dt_start + relativedelta(months=1) + datetime.timedelta(days=-1)
        return [self.dt_start,self.dt_end]

    def set_formset(self):
        '''フォームセット作成'''
        date_range = self.set_date_range()
        account_id = self.request.user
        queryset = ExpenseReport.objects.filter(account_id=account_id,payment_date__range=date_range).order_by('payment_date')
        ExpenseReportFormSet = ExpenseReportForm.create_formset()
        # カラム名__rangeを使うことで日付の範囲指定をする
        formset = ExpenseReportFormSet(
            self.request.POST or None,
            queryset=queryset
            )
        # モデルに金額列が存在しないため、追加する(値は片道は1倍、往復は2倍にする)
        for index,query in enumerate(queryset):
            num = len(formset)
            if index < num:
                fare = query.route.fare
                lap = query.lap
                formset[index].fields['fare'].initial = fare * lap
        # 入力用のフォームにアカウントを紐づける
        for index,form in enumerate(formset):
            formset[index].fields['account'].initial = self.request.user
        return formset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        header = ["日付","科目","相手","目的","経路","往復","金額","","","削除"]
        context['header'] = header
        context['formset'] = self.set_formset()
        context['date_month'] = self.dt.strftime("%Y年%m月")
        context['date'] = self.dt
        return context

    def post(self, request, *args, **kwargs):
        # リダイレクト先の設定
        response = redirect(self.get_success_url())
        get_params = request.POST.urlencode()
        response['location'] += '?' + get_params
        
        formset = self.set_formset()
        if formset.is_valid():
            f = formset.save()
            return response
        else:
            print(formset.errors)
        return response
