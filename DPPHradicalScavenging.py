import glob, csv
import matplotlib.pyplot as plt
import numpy as np

def read_data(filename):
    files = glob.glob(filename)
    all_data = []
    for file in files:
        with open(file, 'r') as f:
            csv_reader = csv.reader(f)
            data = []
            for line in csv_reader:
                if line and not line[0].strip().startswith('#'):
                    data.append([float(val) for val in line])
            all_data = all_data + data                           
    return all_data

def analyze_data(data): # 표준과 분산 구하기
    mean = sum(data) / len(data)
    sum2 = sum([d**2 for d in data])
    var = sum2 / len(data) - mean**2 
    return mean, var

if __name__ == '__main__':
    data_dpph_std = read_data('DPPHabsorbance_standard.csv')
    data_dpph_blank = read_data('DPPHabsorbance_blank.csv')
    data_dpph_sample = read_data('DPPHabsorbance_sample.csv')
    blank = sum([row[0] for row in data_dpph_blank]) / len(data_dpph_blank) # 공실험의 실험값 평균 구하기
    
    std_radicalScavenging_10 = [(1-row[0]/blank)*100 for row in data_dpph_std] # std 10ug/mL 농도의 DPPH 라디칼 제거능력 구하기
    std_radicalScavenging_25 = [(1-row[1]/blank)*100 for row in data_dpph_std] 
    mean_std_10, var_std_10 = analyze_data(std_radicalScavenging_10)
    mean_std_25, var_std_25 = analyze_data(std_radicalScavenging_25)
    samp_radicalScavenging_10 = [(1-row[0]/blank)*100 for row in data_dpph_sample] # sample 10ug/mL 농도의 DPPH 라디칼 제거능력 구하기
    samp_radicalScavenging_25 = [(1-row[1]/blank)*100 for row in data_dpph_sample]
    mean_samp_10, var_samp_10 = analyze_data(samp_radicalScavenging_10)
    mean_samp_25, var_samp_25 = analyze_data(samp_radicalScavenging_25)
    # plot 사용.
    plt.title(f'<variation> \n std_10: {var_std_10:.3f} / std_25: {var_std_25:.3f} \n sample_10: {var_samp_10:.3f} / sample_25: {var_samp_25:.3f}')
    plt.plot(std_radicalScavenging_10, samp_radicalScavenging_10, 'r*', label='10ug/mL')
    plt.plot(std_radicalScavenging_25, samp_radicalScavenging_25, 'g+', label='25ug/mL')
    plt.plot(mean_std_10, mean_samp_10, 'r.', label='mean of 10ug/mL')
    plt.plot(mean_std_25, mean_samp_25, 'g.', label='mean of 25ug/mL')
    plt.xlabel('Ascorbic acid(standard) DPPH radical scavenging(%)')
    plt.ylabel('Jacksal(samples) DPPH radical scavenging(%)')
    plt.legend()
    plt.grid()
    plt.show()
   