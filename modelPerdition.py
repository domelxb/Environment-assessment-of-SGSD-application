import pandas as pd

def calculate_gwp_ap():
    # 使用您提供的GWP和AP数据
    GWP_SGSD_unit = 0.02262       # 一个SGSD的GWP（kg CO₂当量/个）
    AP_SGSD_unit = 0.0139         # 一个SGSD的AP（kg SO₂当量/个）
    GWP_Syringe_unit = 0.888888889  # 一个注射器的GWP（kg CO₂当量/个）
    AP_Syringe_unit = 0.0049      # 一个注射器的AP（kg SO₂当量/个）

    # 使用频率
    syringe_usage_per_year = 365  # 一次性注射器，每天一次
    SGSD_usage_per_year = 52      # SGSD，每周一次

    # 计算每位患者每年的GWP和AP
    GWP_Syringe_patient_year = GWP_Syringe_unit * syringe_usage_per_year
    GWP_SGSD_patient_year = GWP_SGSD_unit * SGSD_usage_per_year

    AP_Syringe_patient_year = AP_Syringe_unit * syringe_usage_per_year
    AP_SGSD_patient_year = AP_SGSD_unit * SGSD_usage_per_year

    # -------------------------------
    # 1. 读取并处理全球各国2040年数据
    # -------------------------------
    path_global_2040 = '/Users/luxiaoxiaobang/Downloads/Beifen/工作/胃滞留药物递送机器人/数学模型-模拟预测影响/原始数据/全球一型糖尿病人数2040年预测.xlsx'
    df_global_2040 = pd.read_excel(path_global_2040)
    # 假设数据包含'Country'和'Patients_2040'列

    # 计算各国2040年的GWP减少量和减少百分比
    df_global_2040['GWP_Syringe_total'] = df_global_2040['Patients_2040'] * GWP_Syringe_patient_year
    df_global_2040['GWP_SGSD_total'] = df_global_2040['Patients_2040'] * GWP_SGSD_patient_year
    df_global_2040['GWP_reduction'] = df_global_2040['GWP_Syringe_total'] - df_global_2040['GWP_SGSD_total']
    df_global_2040['GWP_reduction_percentage'] = (df_global_2040['GWP_reduction'] / df_global_2040['GWP_Syringe_total']) * 100

    # -------------------------------
    # 2. 读取并处理全球七大区域2024-2040年数据
    # -------------------------------
    path_regions = '/Users/luxiaoxiaobang/Downloads/Beifen/工作/胃滞留药物递送机器人/数学模型-模拟预测影响/原始数据/全球七大区域2024-2040的变化.xlsx'
    df_regions = pd.read_excel(path_regions)
    # 假设数据包含'Area'、'2024'到'2040'的年份列

    # 将列名转换为字符串类型
    df_regions.columns = df_regions.columns.map(str)

    # 获取年份列表
    years = [str(year) for year in range(2024, 2041)]

    # 初始化存储GWP计算结果的DataFrame
    gwp_regions = pd.DataFrame()
    gwp_regions['Area'] = df_regions['Area']

    # 对于每个年份，计算GWP总量和减少量
    for year in years:
        patients = df_regions[year]
        # 计算GWP总量
        gwp_regions[f'GWP_Syringe_total_{year}'] = patients * GWP_Syringe_patient_year
        gwp_regions[f'GWP_SGSD_total_{year}'] = patients * GWP_SGSD_patient_year
        # 计算GWP减少量和减少百分比
        gwp_regions[f'GWP_reduction_{year}'] = gwp_regions[f'GWP_Syringe_total_{year}'] - gwp_regions[f'GWP_SGSD_total_{year}']
        gwp_regions[f'GWP_reduction_percentage_{year}'] = (gwp_regions[f'GWP_reduction_{year}'] / gwp_regions[f'GWP_Syringe_total_{year}']) * 100

    # -------------------------------
    # 3. 读取并处理Top 10国家2024-2040年数据
    # -------------------------------
    path_top10_countries = '/Users/luxiaoxiaobang/Downloads/Beifen/工作/胃滞留药物递送机器人/数学模型-模拟预测影响/原始数据/Top 10国家2024-2040的糖尿病人预测.xlsx'
    df_top10 = pd.read_excel(path_top10_countries)
    # 假设数据包含'Income'、'Country'、'2024'到'2040'的年份列

    # 将列名转换为字符串类型
    df_top10.columns = df_top10.columns.map(str)

    # 初始化存储AP计算结果的DataFrame
    ap_results = pd.DataFrame()
    ap_results['Income'] = df_top10['Income']
    ap_results['Country'] = df_top10['Country']

    # 对于每个年份，计算AP总量和减少量
    for year in years:
        patients = df_top10[year]
        # 计算AP总量
        ap_results[f'AP_Syringe_total_{year}'] = patients * AP_Syringe_patient_year
        ap_results[f'AP_SGSD_total_{year}'] = patients * AP_SGSD_patient_year
        # 计算AP减少量和减少百分比
        ap_results[f'AP_reduction_{year}'] = ap_results[f'AP_Syringe_total_{year}'] - ap_results[f'AP_SGSD_total_{year}']
        ap_results[f'AP_reduction_percentage_{year}'] = (ap_results[f'AP_reduction_{year}'] / ap_results[f'AP_Syringe_total_{year}']) * 100

    # -------------------------------
    # 4. 保存计算结果到Excel文件
    # -------------------------------
    with pd.ExcelWriter('计算结果.xlsx') as writer:
        df_global_2040.to_excel(writer, sheet_name='全球各国2040年GWP减少', index=False)
        gwp_regions.to_excel(writer, sheet_name='全球七大区域GWP变化', index=False)
        ap_results.to_excel(writer, sheet_name='Top 10国家AP变化', index=False)

    print("计算完成，结果已保存到'计算结果.xlsx'文件中。")

if __name__ == "__main__":
    calculate_gwp_ap()
