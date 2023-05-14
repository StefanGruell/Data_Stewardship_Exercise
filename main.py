import csv
import matplotlib.pyplot as plt


def read_data(file):
    with open(file, newline='') as csvfile:
        temp_list = []
        reader = csv.reader(csvfile)
        for row in reader:
            temp_list.append(row)
        return temp_list


def filter_gdp_data(raw_data):
    raw_data = filter(lambda x: x[3] != '' and x[3] != 'Country Code', raw_data)
    data = {}
    for entry in raw_data:
        gdp = []
        for i in range(4, 16):
            gdp.append(float(entry[i]) / 10 ** 9)
        data[entry[2]] = gdp
    return dict(sorted(data.items()))


def filter_asparagus_data(raw_data):
    raw_data = filter(lambda x: x[3] != '' and x[3] != 'Area', raw_data)
    data = {}
    for entry in raw_data:
        country = replace_country_names(entry[3])
        if country not in data:
            data[country] = []
        data[country].append(float(entry[11]))
    return dict(sorted(data.items()))


def replace_country_names(country):
    if country.startswith('United Kingdom'):
        country = 'United Kingdom'
    elif country.startswith('United States'):
        country = 'United States'
    elif country.startswith('TÃ¼rkiye'):
        country = 'Turkiye'
    return country


def plot_graph(country_name, data_x, data_y):
    years = []
    for x in range(2011, 2022):
        years.append(x)

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('years')
    ax1.set_ylabel('gpd change in %', color=color)
    ax1.plot(years, data_x[country_name], color=color)
    plt.title(country_name)

    color = 'tab:blue'
    ax2 = ax1.twinx()
    ax2.set_ylabel('area change in %', color=color)
    ax2.plot(years, data_y[country_name], color=color)

    fig.tight_layout()
    plt.show()


def write_csv(data):
    with open('data/results.csv', 'w', newline='') as result_file:
        writer = csv.writer(result_file)
        fields = ['country', 'correlation']
        writer.writerow(fields)
        for row in data.items():
            writer.writerow(row)


if __name__ == '__main__':
    gdp_list = read_data('data/gpd_countries.csv')
    production_list = read_data('data/asparagus_production.csv')
    gdp_list = filter_gdp_data(gdp_list)
    production_list = filter_asparagus_data(production_list)
    matching_countries = []
    for key in production_list.keys():
        if key in gdp_list.keys():
            matching_countries.append(key)
    same_growth_dict = {}
    for country in matching_countries:
        data_x = {}
        data_y = {}

        same_growth = 0.0

        for i in range(1, len(gdp_list[country])):
            if country not in data_x:
                data_x[country] = []
            if country not in data_y:
                data_y[country] = []
            gdp_growth = (gdp_list[country][i] / gdp_list[country][i - 1] - 1) * 100
            data_x[country].append(gdp_growth)
            area_growth = (production_list[country][i] / production_list[country][i - 1] - 1) * 100
            data_y[country].append(area_growth)
            if gdp_growth * area_growth > 0:
                same_growth = same_growth + 1
        plot_graph(country, data_x, data_y)
        same_growth_dict[country] = same_growth / 11
    write_csv(same_growth_dict)
