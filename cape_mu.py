import urllib.request, pandas, csv, math, statistics, datetime, numpy, re
from scipy import stats
ie_data = pandas.read_excel(urllib.request.urlopen('http://www.econ.yale.edu/~shiller/data/ie_data.xls'))
ie = [list(ie_data[col]) for col in ie_data]
def get_cape(i, t1_months): return ie[7][i]/statistics.mean([x for x in ie[9][i - t1_months:i] if not math.isnan(x)])
def get_mu(i, t2, t2_months): return (ie[1][i + t2_months]/ie[1][i])**(1/t2) - 1
def write_pearsonr(file):
	n, w = len(ie[0][6:-1])//12, csv.writer(open(file, 'w', newline = ''))
	for t1 in range(1, n):
		for t2 in range(1, n - t1):
			t1_months, t2_months, log_cape, mu = 12*t1, 12*t2, [], []
			for i in range(6 + t1_months, len(ie[0]) - t2_months - 1):
				log_cape += [math.log(get_cape(i, t1_months))]
				mu += [get_mu(i, t2, t2_months)]
			w.writerow([t1, t2, stats.pearsonr(log_cape, mu)[0]])
def log_reg(t1, t2, file = None):
	if file: w = csv.writer(open(file, 'w', newline = ''))
	t1_months, t2_months, cape_list, mu_list = 12*t1, 12*t2, [], []
	for i in range(6 + t1_months, len(ie[0]) - t2_months - 1):
		year, cape, mu = int(ie[0][i]), math.log(get_cape(i, t1_months)), get_mu(i, t2, t2_months)
		cape_list += [cape]
		mu_list += [mu]
		if file: w.writerow([datetime.datetime(year, int(100*(ie[0][i] - year) + 1/2), 1), cape, mu])
	return numpy.polyfit(cape_list, mu_list, 1)
def mu(t1, t2):
	m, b = log_reg(t1, t2)
	cape0 = get_cape(-2, 12*t1)
	return m*math.log(get_cape(-2, 12*t1)) + b