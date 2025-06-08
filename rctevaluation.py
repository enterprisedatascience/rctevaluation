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
        
        # identify the rows representing treatment and control
        treatment_row = crosstab.iloc[test_cells[0]]
        control_row = crosstab.iloc[test_cells[1]]

        treatment = treatment_row[groupby_feature]
        control = control_row[groupby_feature]

        # extract summary statistics for each group
        counts_control = control_row[feature_size]
        counts_treatment = treatment_row[feature_size]

        mean_control = control_row[feature_mean]
        mean_treatment = treatment_row[feature_mean]

        standard_deviation_control = control_row[feature_std]
        standard_deviation_treatment = treatment_row[feature_std]
        
        t_statistic, p_value = ttest_ind_from_stats(mean1=mean_treatment, std1=standard_deviation_treatment, nobs1=counts_treatment,mean2=mean_control,std2=standard_deviation_control,nobs2=counts_control)
        
        # f-string to print the p value and t statistic
        print(f"The t statistic of the comparison of the treatment test cell of {treatment} compared to the control test cell of {control} for the metric of {metric} is {t_statistic} and the p value is {p_value}.")
        
        #f string to say of the comparison is significant at a given alpha level

        if p_value < alpha: 
            print(f'The comparison between {treatment} and {control} is statistically significant at the threshold of {alpha}') 
        else: 
            print(f'The comparison between {treatment} and {control} is not statistically significant at the threshold of {alpha}')