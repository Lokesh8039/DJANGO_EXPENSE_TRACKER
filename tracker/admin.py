
from django.contrib import admin
from .models import CurrentBalance, TrackingHistory, RequestLogs

admin.site.register(CurrentBalance)
# admin.site.disable_action("delete_selected")

@admin.action(description= "mark selected Expense type as credit")
def mark_credit(modeladmin , request,queryset):
    for q in queryset:
        if q.amount < 0:
            q.amount *= -1
            q.save()
    queryset.update(expense_type = "CREDIT")

@admin.action(description= "mark selected Expense type as debit")
def mark_debit(modeladmin , request,queryset):
    for q in queryset:
        if q.amount > 0:
            q.amount *= -1
            q.save()
    queryset.update(expense_type = "DEBIT")
class Abc(admin.ModelAdmin):
    list_display=[
        "current_balance",
        "amount",
        "expense_type",
        "description",
        "created_at"

    ]
    search_fields = [ "expense_type", "description"]

    list_filter = [ "expense_type"]

    actions = [mark_credit,mark_debit]


admin.site.register(TrackingHistory,Abc)
admin.site.register(RequestLogs)



admin.site.site_header = "Expense Tracker"
admin.site.site_title = "Expense Tracker"
admin.site.site_url = "Expense Tracker"