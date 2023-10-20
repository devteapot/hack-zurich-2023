import pandas as pd
import numpy as np


def main():
    df_arg_in = pd.read_csv('csv/Inbound ARG-Table 1.csv')
    df_arg_out = pd.read_csv('csv/Outbound ARG-Table 1.csv')
    df_mex_in = pd.read_csv('csv/Inbound MEX-Table 1.csv')
    df_mex_out = pd.read_csv('csv/Outbound MEX-Table 1.csv')
    df_arg_in['month'] = [int(i.split('/')[0]) for i in df_arg_in['Date'].to_numpy()]
    df_arg_out['month'] = [int(i.split('/')[1]) for i in df_arg_out['Date'].to_numpy()]
    df_mex_in['month'] = [int(i.split('/')[0]) for i in df_mex_in['Date'].to_numpy()]
    df_mex_out['month'] = [int(i.split('/')[0]) for i in df_mex_out['Date'].to_numpy()]
    a = df_arg_in.groupby('month').size()
    b = df_arg_out.groupby('month').size()
    c = df_mex_in.groupby('month').size()
    d = df_mex_out.groupby('month').size()
    total_month_routes = a + b + c + d
    print(total_month_routes)
    print('Monthly Mean:', int(a.to_numpy().mean()), int(b.to_numpy().mean()), int(c.to_numpy().mean()), int(d.to_numpy().mean()), int(total_month_routes.to_numpy().mean()))
    a = df_arg_in.groupby('Date').size().to_numpy().mean()
    b = df_arg_out.groupby('Date').size().to_numpy().mean()
    c = df_mex_in.groupby('Date').size().to_numpy().mean()
    d = df_mex_out.groupby('Date').size().to_numpy().mean()
    mean_routes_day = int((a + b + c + d) / 4)
    print('Routes mean per day:', int(a), int(b), int(c), int(d), mean_routes_day)


if __name__ == '__main__':
    main()