from django.shortcuts import render

from apps.calculation_data_app.forms import ReimbursementValueForm


def insert_reimbursements(request):
    if request.method == 'POST':
        form = ReimbursementValueForm(request.POST)

        if form.is_valid():
            form.save()
    else:
        form = ReimbursementValueForm()

    return render(request, 'reimbursements.html',
                  {'form': form})
