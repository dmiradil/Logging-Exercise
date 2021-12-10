### Python App that generates a report
### that ranks the top browsers and their versions in descending order
### Info: this is a vanilla Python3 app, it does not require any dependencies or imports
### to run: '$ python3 browser.py'

log_file = './lb.log'
browsers = {'Safari': [], 'Chrome': [], 'Firefox': [], 'Trident': []}

def is_chrome(user_agent):
    return 'Chrome' in user_agent
def is_ie(user_agent):
    return 'Trident' in user_agent
def is_firefox(user_agent):
    return 'Firefox' in user_agent
def is_safari(user_agent):
    if 'Chrome' in user_agent:
        return False
    elif 'Safari' in user_agent:
        return True
    else:
        return False

def is_valid_browser_user_agent(line):
    if 'Apache-HttpClient' in line or 'UptimeRobot/2.0' in line:
        return False

def get_versions_count(list_of_versions):
    versions_counter = {}
    for version in list_of_versions:
        if version in versions_counter.keys():
            versions_counter[version] += 1
        else:
            versions_counter[version] = 1
    return sorted([(value,key) for (key,value) in versions_counter.items()])

def get_most_popular_browser(browsers):
    counted_browsers = {}

    for key in browsers.keys():
        counted_browsers[key] = len(browsers[key])
    return sorted([(value,key) for (key,value) in counted_browsers.items()])

def get_browser_version(agent_data, browser):
    for item in agent_data:
        if browser in item:
            if browser == 'Trident':
                return item.split('/')[1].split(')')[0]
            elif browser == 'Safari':
                return item.split('/')[1].split('"')[0]
            elif browser == 'Firefox':
                return item.split('/')[1].split(')')[0].split('"')[0]
            elif browser == 'Chrome':
                return item.split('/')[1]
            else:
                raise Exception('not a browser user agent')

def get_browsers_data_from_logs(log):
    with open(log) as file:
        for line in file.readlines():
            if is_valid_browser_user_agent(line):
                continue

            if is_chrome(line):

                browsers['Chrome'].append(get_browser_version(line.split()[14:28],'Chrome'))
                continue
            if is_firefox(line):

                browsers['Firefox'].append(get_browser_version(line.split()[14:28],'Firefox'))
                continue
            if is_ie(line):

                browsers['Trident'].append(get_browser_version(line.split()[14:25],'Trident'))
                continue
            if is_safari(line):

                browsers['Safari'].append(get_browser_version(line.split()[14:28],'Safari'))
                continue

        browsers_by_popularity = get_most_popular_browser(browsers)

        browsers['Safari'] = get_versions_count(browsers['Safari'])
        browsers['Chrome'] = get_versions_count(browsers['Chrome'])
        browsers['Firefox'] = get_versions_count(browsers['Firefox'])
        browsers['Trident'] = get_versions_count(browsers['Trident'])

        print('Browsers by popularity:')
        for browser in browsers_by_popularity[::-1]:
            print(f'{browser[1]} user agents - "{browser[0]}"')
            if browser[1] in browsers.keys():
                for version in browsers[browser[1]][::-1]:
                  print(f'\tv{version[1]} calls - "{version[0]}"')
            print('\n')



if __name__ == "__main__":
  get_browsers_data_from_logs(log_file)