'''
reference repo: https://github.com/Carven12/alispider
'''
import requests
import json
import pprint

def http_get_json(url, params=None):
    # 设置请求头，注明请求发出原地址
    headers = {'Referer': "https://tco.aliyun.com/tco/ecs/calculator?spm=5176.8030368.1058474.1.22c43aa4TZEd79"}
    # 发起请求,获取返回的json
    response = requests.get(url, headers=headers, params=params).json()
    return response

def get_platform_info():
    # 跨域请求地址
    request_url = 'https://ecs-buy.aliyun.com/api/ecsCommodity/getCommodity.jsonp?commodityCode=vm&orderType=BUY'

    response = http_get_json(request_url)
    # 获取地区名及相应代号
    region_list = response['data']['components']['vm_region_no']['vm_region_no']
    # 获取所有虚拟机规格
    vm_list = response['data']['components']['instance_type']['instance_type']

    return dict(region_list=region_list, vm_list=vm_list)

def get_price_by_name(region, vm):
    # 设置请求参数
    components = {
        "instances": [{
            "RegionId": region['value'],
            "ZoneId": "random",
            "NetworkType": "vpc",
            "IoOptimized": True,
            "InstanceType": vm['value'],
            "SystemDiskSize": 20,
            "SystemDiskCategory": "cloud_efficiency",
            "PriceUnit": "Month",
            "Period": 1,
            "Amount": 1
        }],
        "disks": [],
        "bandwidths": [{
            "RegionId": region['value'],
            "InternetMaxBandwidthOut": 0,
            "InternetChargeType": "PayByBandwidth",
            "PriceUnit": "Month",
            "Period": 1,
            "Amount": 1
        }]
    }
    payload = {
        'components': json.dumps(components)
    }

    # 设置请求价格的url
    request_price_url = 'https://tco.aliyun.com/tco/ecs/price.json'

    response_price = http_get_json(request_price_url, params=payload)

    if response_price is not None:
        result_price = response_price['data']['instances'][0]['data']['tradePrice']
        # print(result_price)
        return result_price
    else:
        print('所选区域中该配置的虚拟机不存在！')
        return None

class Aliyun():
    @classmethod
    def list_region(cls):
        platform = get_platform_info()
        return platform['region_list']
    @classmethod
    def list_vm(cls):
        platform = get_platform_info()
        return platform['vm_list']
    @classmethod
    def get_price_by_name(cls, region_id, vm_id):
        region = dict(value=region_id)
        vm = dict(value=vm_id)
        return get_price_by_name(region, vm)
    @classmethod
    def get_price_by_spec(cls, region_id, cpu, memory):
        region = dict(value=region_id)
        def fn(x):
            return (float(x.get('cpu', 0)) == cpu) and (float(x.get('memory', 0)) == memory)
        vm_list = filter(fn, cls.list_vm())
        result = []
        for vm in vm_list:
            price = get_price_by_name(region, vm)
            # print(vm, price)
            result.append(dict(vm_name=vm['value'], price=price))
        return result

def main():
    # 循环遍历
    platform = get_platform_info()
    for region in platform['region_list']:
        for vm in platform['vm_list']:
            price_info = get_price_by_name(region, vm)
            pprint.pprint(price_info)
            

if __name__ == '__main__':
    main()