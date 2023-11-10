import pandas as pd
import numpy as np
import os
from datetime import datetime, date, timedelta
from pathlib import Path
import plotly.express as px
import plotly
import plotly.graph_objects as go

pd.set_option('display.width', 500)
pd.set_option('display.max_rows', 2000)
pd.set_option('display.max_columns', 20)


def combine_all_data(filename):
        # ============================================ KSE 100==========================================================
        df = pd.read_csv(filename)

        #Rename columns
        df.rename(columns={'Date': 'date',
                                   'Close': 'kse_100_close', 
                                   'Volume': 'kse_100_volume', 
                                   'Trade Value Sum': 'uin_trade_value',
                                   'UIN Percentage': 'uin_pct', 
                                   'NET values_all fipi sectors': 'net_value_foreign_investors',
                                   'Price': 'usd_price', 
                                   'lipi_all': 'all_other_lipis', 
                                   'lipi_broker': 'brokers_individuals', 
                                   'sum_mts': 'mts_amount',
                                   'usd_change_pct': 'usd_change_pct',
                                   'open_interest': 'open_interest'}, inplace=True)

        df['date'] = pd.to_datetime(df['date'])
        df['kse_100_mv10'] = df['kse_100_close'].rolling(10).mean()

        #Convert all columns to float
        df[['kse_100_close', 'kse_100_volume', 'uin_trade_value', 'uin_pct', 'net_value_foreign_investors', 'usd_price', 'all_other_lipis', 'brokers_individuals', 'mts_amount', 'usd_change_pct', 'open_interest']] = df[
            ['kse_100_close', 'kse_100_volume', 'uin_trade_value', 'uin_pct', 'net_value_foreign_investors', 'usd_price', 'all_other_lipis', 'brokers_individuals', 'mts_amount', 'usd_change_pct', 'open_interest']].astype(float)
        
        # ===========================================GETTING VOLATILITY OF KSE 100 INDEX AND ROLLING AVG ====================================================================
        df = get_volatility_index(df)
        df['kse_100_volatility'] = df['kse_100_volatility'].astype(float)
        df['kse_100_vol_mv10'] = df['kse_100_volatility'].rolling(10).mean()

        # ============================================ UIN ========================================================
        #Calculate moving averages of uin
        df['uin_trade_mv10'] = df['uin_trade_value'].rolling(10).mean()


        # ============================================= CM  ============================================================
        # df_cm = pd.read_csv(os.path.join(self.processed_data_dir, 'sett-info-cm-wise-after-2015.csv'), usecols=['date',
        #                                                                                                         'cm_trade_value',
        #                                                                                                         'cm_settlement_value'])
        # df_cm['date'] = pd.to_datetime(df_cm['date'])
        # # df_cm = df_cm[df_cm['date'] >= datetime(2016, 1, 1)]
        # df_cm[['cm_trade_value', 'cm_settlement_value']] = df_cm[['cm_trade_value', 'cm_settlement_value']].astype(
        #     float)

        # ===============================================================================================================


        # ==============================================================================================================
        df['mts_amount'] = df['mts_amount'].interpolate()
        df['mts_amount_mv10'] = df['mts_amount'].rolling(10).mean()

        # ==============================================================================================================
        df[['net_value_foreign_investors', 'brokers_individuals', 'all_other_lipis']] = df[
            ['net_value_foreign_investors', 'brokers_individuals', 'all_other_lipis']].interpolate()

        df['net_value_foreign_investors_mv10'] = df['net_value_foreign_investors'].rolling(10).mean()
        df['brokers_individuals_mv10'] = df['brokers_individuals'].rolling(10).mean()
        df['all_other_lipis_mv10'] = df['all_other_lipis'].rolling(10).mean()
        # print(df.dtypes)

        # ==============================================================================================================
        df['open_interest'] = df['open_interest'].interpolate()
        df['open_interest_mv10'] = df['open_interest'].rolling(10, min_periods=5).mean()

        # ==============================================================================================================
        # df_tbills = pd.read_csv(os.path.join(self.processed_data_dir, 'tbills.csv'), parse_dates=['date'])
        # df_tbills.rename(columns={'realized_amount': 'tbills_price'}, inplace=True)
        # df_tbills['tbills_change_pct'] = df_tbills['tbills_price'].pct_change()
        # df_tbills['date'] = pd.to_datetime(df_tbills['date'])
        # df_tbills['tbills_mv10'] = df_tbills['tbills_price'].rolling(10).mean()
        # df_tbills.drop(columns=['check'], inplace=True)

        # ==============================================================================================================

        df['usd_pkr_mv10'] = df['usd_price'].rolling(10).mean()

        print(df.tail(5))

        #Already calculated when collecting data
        # df['uin_pct'] = df['uin_settlement_value'].astype(float) / df['uin_trade_value'].astype(
        #     float)
        # df['cm_pct'] = df['cm_settlement_value'] / df['cm_trade_value']
        # df['mts_amount'] = df['net_open_position_value'] + df['net_open_mts_amount']

        

        # df.drop(columns=['uin_settlement_value', 'cm_settlement_value', 'cm_trade_value',
        #                          'net_open_position_value', 'net_open_mts_amount'], inplace=True)

        df['target'] = np.where(df['kse_100_pct_change'] > 0, 1, 0)
        df['target'] = df['target'].shift(-1)

        # df = df[df['date'] >= datetime(2016, 1, 1)]

        print(df.head(5))
        print('===============+=======================================================================================')
        print(df[df.isnull().any(axis=1)])

        df = df.sort_values(by=['date'])
        df.to_csv(os.path.join(self.processed_data_dir, 'combined_data.csv'), index=False)

def get_volatility_index(self, kse_file): #kse_file is dataframe, function return the dataframe with kse_100_volatility
    df_test = kse_file
    # df_test = pd.read_csv(os.path.join(self.processed_data_dir, kse_file))
    print('Length before: ', len(df_test))
    df_test.drop_duplicates(subset=['date'], inplace=True)
    print('Length after: ', len(df_test))
    df_test['date'] = pd.to_datetime(df_test['date'])
    print(df_test.head(5))

    kse_type = kse_file.split(".")[0]
    df_test['kse_100_volatility'] = ((np.log(df_test['High']) - np.log(df_test['Open'])) * (
                np.log(df_test['High']) - np.log(df_test['Close']))) + (
                                                    (np.log(df_test['Low']) - np.log(df_test['Open'])) * (
                                                        np.log(df_test['Low']) - np.log(df_test['Close'])))

    # df_test[['date', 'kse_100_volatility']].to_csv(
    #     os.path.join(self.processed_data_dir, f'{kse_type}_volatility.csv'), index=False)

    return df_test
    
def feature_selection(self):
    df_test = pd.read_csv(os.path.join(self.processed_data_dir, 'combined_data.csv'))
    cols = list(df_test)
    # remove_features = ['tbills_price', 'cm_pct', 'tbills_mv10', 'usd_change_pct']

    remove_features = ['tbills_price', 'cm_pct', 'tbills_mv10', 'usd_change_pct', 'usd_price', 'usd_pkr_mv10',
                        'open_interest_mv10', 'kse_100_mv10', 'mts_amount_mv10', 'uin_trade_mv10',
                        'all_other_lipis', 'kse_100_mv10', 'mts_amount']

    kse_all_features = [col for col in cols if col.startswith('kse_all')]
    remove_features.extend(kse_all_features)
    new_cols = [col for col in cols if col not in remove_features]
    print('Total Features Before: ', len(cols))
    print('Remove these features: ', remove_features)
    print('Total New Features: ', len(new_cols))
    print('New Features: ', new_cols)
    df_test = df_test[new_cols]
    print(df_test.head(5))
    df_test['date'] = pd.to_datetime(df_test['date'])

    cols_with_missing_vals = ['net_value_foreign_investors', 'brokers_individuals', 'all_other_lipis',
                                'net_value_foreign_investors_mv10', 'brokers_individuals_mv10',
                                'all_other_lipis_mv10',
                                'open_interest', 'open_interest_mv10']
    fill_cols = [col for col in cols_with_missing_vals if col in df_test.columns]

    df_test[fill_cols] = df_test[fill_cols].interpolate()

    df_test = df_test[(df_test['date'] >= datetime(2016, 1, 14)) & (df_test['date'] <= datetime(2021, 4,
                                                                                                19))]  # Fipi Lipi features have data from 2016,1,1 and 10 day moving avg creates null initially
    print(df_test.isnull().sum())

    df_test.to_csv(os.path.join(self.processed_data_dir, 'combined_filtered_data_14_feat.csv'), index=False)

def correlation_ratio(self, categorical_column, numeric_column):
    fcat, _ = pd.factorize(categorical_column)
    cat_num = np.max(fcat) + 1
    y_avg_array = np.zeros(cat_num)
    n_array = np.zeros(cat_num)
    for i in range(0, cat_num):
        cat_measures = numeric_column[np.argwhere(fcat == i).flatten()]
        n_array[i] = len(cat_measures)
        y_avg_array[i] = np.average(cat_measures)
    y_total_avg = np.sum(np.multiply(y_avg_array, n_array)) / np.sum(n_array)
    print('Y total avg: ', y_total_avg)
    numerator = np.sum(np.multiply(n_array, np.power(np.subtract(y_avg_array, y_total_avg), 2)))
    denominator = np.sum(np.power(np.subtract(numeric_column, y_total_avg), 2))
    if numerator == 0:
        eta = 0.0
    else:
        print(f'Dividing: {numerator}/{denominator}')
        eta = np.sqrt(numerator / denominator)
    return eta

def find_correlation(self):
    df_test = pd.read_csv(os.path.join(self.processed_data_dir, 'combined_filtered_data_14_feat.csv'))
    cols = [col for col in df_test.columns if col not in ['date']]
    df_test = df_test[cols]
    print(df_test.head(5))
    print('=' * 100)
    corr = df_test.corr()
    print(corr)
    print('==================================')

    # mask = np.zeros_like(corr, dtype=np.bool)
    # mask[np.triu_indices_from(mask)] = True
    #
    # # Set up the matplotlib figure
    # f, ax = plt.subplots(figsize=(11, 9))
    #
    # # Generate a custom diverging colormap
    # cmap = sns.diverging_palette(220, 10, as_cmap=True)
    # # cmap = sns.diverging_palette(20, 220, n=400)
    #
    # # Draw the heatmap with the mask and correct aspect ratio
    # ax = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, center=0,
    #                  square=True, linewidths=.5, cbar_kws={"shrink": .7})
    # ax.set_xticklabels(
    #     ax.get_xticklabels(),
    #     rotation=45,
    #     horizontalalignment='right'
    # )
    # plt.show()
    #
    corr = corr.round(2)

    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    corr = corr.where(mask)

    df_copy = corr.copy(deep=True)
    df_copy = df_copy[((df_copy >= 0.8) | (df_copy <= -0.8)) & (df_copy != 1)]

    high_corr = []
    for col in df_copy.columns:
        s = df_copy[col].dropna()
        if not df_copy.empty:
            tmp = [[col, val, s.loc[val]] for val in s.index.values]
            high_corr.extend(tmp)

    print('High Correlations (more than 8): ', high_corr)

    df_high_corr = pd.DataFrame(data=high_corr, columns=['feat_1', 'feat_2', 'corr'])
    df_high_corr.sort_values(by=['feat_1'], inplace=True)
    print(df_high_corr)

    fig = go.Figure(go.Heatmap(
        z=corr,
        x=corr.columns,
        y=corr.columns,
        colorscale=px.colors.diverging.RdBu,  # px.colors.sequential.Blues, #px.colors.diverging.RdBu
        zmin=-1,
        zmax=1
    )
    )
    fig.update_layout(title='Correlation of features')
    plotly.offline.plot(fig, filename=os.path.join(self.processed_data_dir,
                                                    'correlation_combined_filtered_data_14_feat_plotly.html'))