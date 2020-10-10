def calculate_months_hours_fund(accounted_period_start: str, HourFund: object):
       
        acc_period_year = str(accounted_period_start)[0:4]
        acc_period_month = str(accounted_period_start)[5:7]
        
        monthly_hours_fund_id = HourFund.objects.get(year = acc_period_year, month = acc_period_month)
        
        return monthly_hours_fund_id.total_hours