def aggregate_and_ttest(dataset, groupby_feature='province', alpha=.05, test_cells = [0, 1]):
    #Imports
    from tqdm import tqdm
    from scipy.stats import ttest_ind_from_stats

    
    metrics = ['gdp', 'fdi', 'it']
    
    feature_size = 'size'
    feature_mean = 'mean'
    feature_std = 'std'    

    for metric in tqdm(metrics):
        
        #print(metric)
        crosstab = dataset.groupby(groupby_feature, as_index=False)[metric].agg(['size', 'mean', 'std'])
        print(crosstab)
        
        treatment = crosstab.index[test_cells[0]]
        control = crosstab.index[test_cells[1]]
        
        counts_control = crosstab.loc[control, feature_size]
        counts_treatment = crosstab.loc[treatment, feature_size]

        mean_control = crosstab.loc[control, feature_mean]
        mean_treatment = crosstab.loc[treatment, feature_mean]

        standard_deviation_control = crosstab.loc[control, feature_std]
        standard_deviation_treatment = crosstab.loc[treatment, feature_std]
        
        t_statistic, p_value = ttest_ind_from_stats(mean1=mean_treatment, std1=standard_deviation_treatment, nobs1=counts_treatment,mean2=mean_control,std2=standard_deviation_control,nobs2=counts_control)
        
        #fstring to print the p value and t statistic
        print(f"The t statistic of the comparison of the treatment test cell of {treatment} compared to the control test cell of {control} for the metric of {metric} is {t_statistic} and the p value is {p_value}.")
        
        #f string to say of the comparison is significant at a given alpha level

        if p_value < alpha: 
            print(f'The comparison between {treatment} and {control} is statistically significant at the threshold of {alpha}') 
        else: 
            print(f'The comparison between {treatment} and {control} is not statistically significant at the threshold of {alpha}')