import copy

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from matplotlib.colors import LinearSegmentedColormap,BoundaryNorm
import os
from matplotlib.lines import Line2D
BASE_SAVE_DIR = "/home/hc/code/TCPN-F/problem_identity_cases"


def colormap():
    # 定义自定义colormap的颜色列表，这里使用RGB值
    # colors = ['#fefffe', '#b2d0dd', '#97bcd6', '#799ec2', '#6ca45e',
    #           '#89b95e','#a7c17f','#e5f35b','#e7bd60','#e07066',
    #           '#e16a94','#dc5f9b','#b65dbf','#5743ec','#1c125b']  # 6个颜色
    # colors = [
    #     "#FFFFFF",  # 0 mm - 白色
    #     "#B9E1F5",  # 20-50 mm - 浅蓝色
    #     "#71B1D1",  # 50-100 mm - 蓝色
    #     "#50A25A",  # 100-150 mm - 绿色
    #     "#97C559",  # 150-200 mm - 黄绿色
    #     "#F3A646",  # 200-250 mm - 橙色
    #     "#E8683F",  # 250-300 mm - 红色
    #     "#D13B8C",  # 300-400 mm - 粉红色
    #     "#5950B2",  # 400-500 mm - 紫色
    #     "#1C3089",  # 500-550 mm - 深蓝色
    #     "#000032"  # >550 mm - 深色
    # ]

#for show
    colors = [
        "#FFFFFF",  # 0 mm - 白色
        "#B9E1F5",  # 20-50 mm - 浅蓝色
        "#71B1D1",  # 50-100 mm - 蓝色
        "#50A25A",  # 100-150 mm - 绿色
        "#97C559",  # 150-200 mm - 黄绿色
        "#F3A646",  # 200-250 mm - 橙色
        "#E8683F",  # 250-300 mm - 红色
        "#D13B8C",  # 300-400 mm - 粉红色
        "#5950B2",  # 400-500 mm - 紫色
        "#1C3089",  # 500-550 mm - 深蓝色
        "#000032"  # >550 mm - 深色
    ]

    # bounds = [20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    bounds = [10, 20, 40, 60, 80, 100, 125, 150, 200, 400, 450, 500, 550]
    # 定义colormap的分段点，范围在0到1之间，对应颜色列表中的颜色
    # bounds = [0, 1, 2, 3, 5,
    #           7, 10, 15, 20, 25,
    #           30,40,50,70,100,150]
    # bounds = [40,60, 80, 100, 120, 140,
    #           160, 180, 200, 250, 300, 350, 400,450,500,550]

    # 创建自定义colormap
    cmap = LinearSegmentedColormap.from_list('custom_colormap', colors, N=256)
    norm = BoundaryNorm(bounds, cmap.N, clip=True)
    return cmap,norm

def colormap_single():
    # 定义自定义colormap的颜色列表，这里使用RGB值
    colors = ['#fefffe', '#b2d0dd', '#97bcd6', '#799ec2', '#6ca45e',
              '#89b95e','#a7c17f','#e5f35b','#e7bd60','#e07066',
              '#e16a94','#dc5f9b','#b65dbf','#5743ec','#1c125b']  # 6个颜色


    # bounds = [20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]

    # 定义colormap的分段点，范围在0到1之间，对应颜色列表中的颜色
    bounds = [0, 1, 2, 3, 5,
              7, 10, 15, 20, 25,
              30,40,50,70,100,150]


    # 创建自定义colormap
    cmap = LinearSegmentedColormap.from_list('custom_colormap', colors, N=256)
    norm = BoundaryNorm(bounds, cmap.N, clip=True)
    return cmap,norm

def show_range(typhoon_path_lon,typhoon_path_lat):
    lon_max = np.max(typhoon_path_lon)
    lon_min = np.min(typhoon_path_lon)
    lat_max = np.max(typhoon_path_lat)
    lat_min = np.min(typhoon_path_lat)
    # if lon_max+10>180:
    #     area_max = lon_max + 10-360
    #     return lon_min-10,lon_max+10,lat_min-10,area_max
    # else:
    return lon_min-6,lon_max+6,lat_min-6,lat_max+6


def show_accumulate_rainfall(track=None,rainfall_data=None):
    '''
    检查降雨的分布   上面是高纬度，下面是低纬度？？？？？？？？
    :param track: 台风轨迹
    :param rainfall_data: 台风降雨
    :return:
    '''
    # 假设我们有台风路径的经纬度和降雨数据（以示例数据代替）
    # 台风路径经纬度
    cmap, norm = colormap()
    typhoon_path_lon = track[:,0]
    typhoon_path_lat = track[:,1]
    # typhoon_path_lon = [-90, -88, -86, -84, -82]
    # typhoon_path_lat = [20, 21, 22, 23, 24]
    # rainfall_data = [np.random.rand(100, 100) * 100 for _ in range(len(typhoon_path_lon))]




    #   这里的经度不能大于180  大于180就变成负的了
    lon_min,lon_max,lat_min,lat_max = show_range(typhoon_path_lon,typhoon_path_lat)
    grid_resolution = 10/64  # 设置网格分辨率（单位：度）
    lon_grid = np.arange(lon_min, lon_max, grid_resolution)
    lat_grid = np.arange(lat_min, lat_max, grid_resolution)
    accumulated_precipitation = np.zeros((len(lat_grid), len(lon_grid)))


    # 累积降雨数据
    for step in range(len(typhoon_path_lon)):
        # if step >0:
        #     continue
        # 获取每个 step 的降雨数据及其覆盖的经纬度范围
        step_lon = np.linspace(typhoon_path_lon[step] - 5, typhoon_path_lon[step] + 5, rainfall_data[step].shape[1])
        step_lat = np.linspace(typhoon_path_lat[step] - 5, typhoon_path_lat[step] + 5, rainfall_data[step].shape[0])

        # 找到大网格中对应的索引范围
        lon_indices = np.searchsorted(lon_grid, step_lon)
        lat_indices = np.searchsorted(lat_grid, step_lat)

        # 将降雨数据累加到对应位置
        flipped_arr = np.flip(rainfall_data[step], axis=0)
        for i, lat_idx in enumerate(lat_indices):
            for j, lon_idx in enumerate(lon_indices):
                # if accumulated_precipitation[lat_idx, lon_idx]<flipped_arr[i, j]:
                #     accumulated_precipitation[lat_idx, lon_idx] = flipped_arr[i, j]
                accumulated_precipitation[lat_idx, lon_idx] += flipped_arr[i, j]*2

    # 创建地图
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([lon_min,lon_max,lat_min,lat_max], crs=ccrs.PlateCarree())  # 设置地图范围

    # 添加地图特征
    ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

    # 绘制降雨数据
    # for step in range(np.shape(typhoon_path_lon)[0]):
    #     if step > 0:
    #         continue
    #     # 降雨数据示例，假设降雨范围为10°x10°
    #     # rainfall_data = np.random.rand(10, 10) * 100  # 随机生成示例降雨数据
    #     rainfall_lon = np.linspace(typhoon_path_lon[step] - 5, typhoon_path_lon[step] + 5, 64)
    #     rainfall_lat = np.linspace(typhoon_path_lat[step] - 5, typhoon_path_lat[step] + 5, 64)
    #     lon_grid, lat_grid = np.meshgrid(rainfall_lon, rainfall_lat)
    #     ax.contourf(lon_grid, lat_grid, np.flip(rainfall_data[step], axis=0), transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, alpha=0.7)



    lon_grid_2d, lat_grid_2d = np.meshgrid(lon_grid, lat_grid)
    contour = ax.contourf(lon_grid_2d, lat_grid_2d, accumulated_precipitation, transform=ccrs.PlateCarree(),
                          cmap=cmap, norm=norm, alpha=0.7)
    plt.colorbar(contour, ax=ax, orientation='vertical', label="Accumulated Precipitation (mm)")

    # 绘制台风路径
    ax.plot(typhoon_path_lon, typhoon_path_lat, color='black', linewidth=2, label="Typhoon Path")
    ax.scatter(typhoon_path_lon, typhoon_path_lat, color='red', s=3)  # 标记台风中心点

    # 添加标题和图例
    plt.title("Typhoon Path and Surrounding Rainfall")
    plt.legend()

    plt.show()

def show_accumulate_rainfall_all_old(track_list=None,rainfall_data_list=None,titile_list=None,file_name=None):
    '''
    检查降雨的分布   上面是高纬度，下面是低纬度？？？？？？？？
    :param track: 台风轨迹
    :param rainfall_data: 台风降雨
    :return:
    '''
    # 假设我们有台风路径的经纬度和降雨数据（以示例数据代替）
    # 台风路径经纬度
    cmap, norm = colormap()
    fig, axes = plt.subplots(1, len(track_list), figsize=(len(track_list) * 10, 1 * 10), dpi=100,subplot_kw={'projection': ccrs.PlateCarree()})
    for fig_i,(track,rainfall_data) in enumerate(zip(track_list,rainfall_data_list)):
        typhoon_path_lon = track[:,0]
        typhoon_path_lat = track[:,1]
        # typhoon_path_lon = [-90, -88, -86, -84, -82]
        # typhoon_path_lat = [20, 21, 22, 23, 24]
        # rainfall_data = [np.random.rand(100, 100) * 100 for _ in range(len(typhoon_path_lon))]




        #   这里的经度不能大于180  大于180就变成负的了
        lon_min,lon_max,lat_min,lat_max = show_range(track_list[0][:,0],track_list[0][:,1])
        grid_resolution = 10/64  # 设置网格分辨率（单位：度）
        lon_grid = np.arange(lon_min, lon_max, grid_resolution)
        lat_grid = np.arange(lat_min, lat_max, grid_resolution)
        accumulated_precipitation = np.zeros((len(lat_grid), len(lon_grid)))


        # 累积降雨数据
        for step in range(len(typhoon_path_lon)):
            # if step >0:
            #     continue
            # 获取每个 step 的降雨数据及其覆盖的经纬度范围
            step_lon = np.linspace(typhoon_path_lon[step] - 5, typhoon_path_lon[step] + 5, rainfall_data[step].shape[1])
            step_lat = np.linspace(typhoon_path_lat[step] - 5, typhoon_path_lat[step] + 5, rainfall_data[step].shape[0])

            # 找到大网格中对应的索引范围
            lon_indices = np.searchsorted(lon_grid, step_lon)
            lat_indices = np.searchsorted(lat_grid, step_lat)

            # 将降雨数据累加到对应位置
            flipped_arr = np.flip(rainfall_data[step], axis=0)
            for i, lat_idx in enumerate(lat_indices):
                for j, lon_idx in enumerate(lon_indices):
                    # if accumulated_precipitation[lat_idx, lon_idx]<flipped_arr[i, j]:
                    #     accumulated_precipitation[lat_idx, lon_idx] = flipped_arr[i, j]
                    accumulated_precipitation[lat_idx, lon_idx] += flipped_arr[i, j]*2

        # 创建地图
        # fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
        axes[fig_i].set_extent([lon_min,lon_max,lat_min,lat_max], crs=ccrs.PlateCarree())  # 设置地图范围
        axes[fig_i].set_title(titile_list[fig_i], fontsize=20, y=0.98)
        # 添加地图特征
        axes[fig_i].add_feature(cfeature.LAND, zorder=0, edgecolor='black')
        axes[fig_i].add_feature(cfeature.COASTLINE, linewidth=2)
        gl = axes[fig_i].gridlines(draw_labels=True, color='gray', linestyle='--', alpha=0.5)
        gl.top_labels = False  # 不显示顶部的纬度标签
        gl.right_labels = False  # 不显示右侧的经度标签

        # 绘制降雨数据
        # for step in range(np.shape(typhoon_path_lon)[0]):
        #     if step > 0:
        #         continue
        #     # 降雨数据示例，假设降雨范围为10°x10°
        #     # rainfall_data = np.random.rand(10, 10) * 100  # 随机生成示例降雨数据
        #     rainfall_lon = np.linspace(typhoon_path_lon[step] - 5, typhoon_path_lon[step] + 5, 64)
        #     rainfall_lat = np.linspace(typhoon_path_lat[step] - 5, typhoon_path_lat[step] + 5, 64)
        #     lon_grid, lat_grid = np.meshgrid(rainfall_lon, rainfall_lat)
        #     ax.contourf(lon_grid, lat_grid, np.flip(rainfall_data[step], axis=0), transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, alpha=0.7)



        lon_grid_2d, lat_grid_2d = np.meshgrid(lon_grid, lat_grid)
        contour = axes[fig_i].contourf(lon_grid_2d, lat_grid_2d, accumulated_precipitation, transform=ccrs.PlateCarree(),
                               cmap=cmap, norm=norm, alpha=0.7)


        # 绘制台风路径
        if fig_i == 0:
            # axes[fig_i].plot(typhoon_path_lon, typhoon_path_lat, color='black', linewidth=2)
            axes[fig_i].scatter(typhoon_path_lon, typhoon_path_lat, color='black', s=10)  # 标记台风中心点
        else:
            # axes[fig_i].plot(typhoon_path_lon, typhoon_path_lat, color='black', linewidth=2)
            axes[fig_i].scatter(typhoon_path_lon, typhoon_path_lat, color='red', s=10)  # 标记台风中心点
            # axes[fig_i].plot(track_list[0][:,0],track_list[0][:,1], color='black', linewidth=2)
            axes[fig_i].scatter(track_list[0][:,0],track_list[0][:,1], color='black', s=10)  # 标记台风中心点

        # 添加标题和图例
        # plt.title("Typhoon Path and Surrounding Rainfall")
        # plt.legend()

    # plt.colorbar(contour, ax=axes[fig_i], orientation='vertical', label="Accumulated Precipitation (mm)")
    plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.25, wspace=0.2, hspace=0.15)
    cbar_ax = fig.add_axes([0.15, 0.15, 0.7, 0.03])
    cbar = fig.colorbar(contour, cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Accumulated Precipitation (mm)', fontsize=20)
    plt.show()
    os.makedirs('Accumulated_Precipitation',exist_ok=True)
    plt.savefig(os.path.join('Accumulated_Precipitation',file_name+'.png'))
    plt.close()



def show_accumulate_rainfall_all(track_list=None, rainfall_data_list=None, title_list=None, file_name=None,track_predictor=None,only_track=False):
    cmap, norm = colormap()
    fig, axes = plt.subplots(1, len(track_list), figsize=(len(track_list) * 5, 5), dpi=100,
                             subplot_kw={'projection': ccrs.PlateCarree()})

    for fig_i, (track, rainfall_data) in enumerate(zip(track_list, rainfall_data_list)):
        if track.shape[0]<2:
            continue
        typhoon_path_lon = track[:, 0]
        typhoon_path_lat = track[:, 1]

        # 设置地图范围和网格
        lon_min, lon_max, lat_min, lat_max = show_range(track_list[0][:, 0], track_list[0][:, 1])
        grid_resolution = 10 / 64
        lon_grid = np.arange(lon_min, lon_max, grid_resolution)
        lat_grid = np.arange(lat_min, lat_max, grid_resolution)
        accumulated_precipitation = np.zeros((len(lat_grid), len(lon_grid)))

        # 累积降雨数据
        for step in range(len(typhoon_path_lon)):
            step_lon = np.linspace(typhoon_path_lon[step] - 5, typhoon_path_lon[step] + 5, rainfall_data[step].shape[1])
            step_lat = np.linspace(typhoon_path_lat[step] - 5, typhoon_path_lat[step] + 5, rainfall_data[step].shape[0])

            lon_indices = np.searchsorted(lon_grid, step_lon)
            lat_indices = np.searchsorted(lat_grid, step_lat)
            flipped_arr = np.flip(rainfall_data[step], axis=0)

            for i, lat_idx in enumerate(lat_indices):
                for j, lon_idx in enumerate(lon_indices):
                    if title_list[fig_i] == 'ECMWF':
                        accumulated_precipitation[lat_idx, lon_idx] += flipped_arr[i, j] * 4
                    else:
                        accumulated_precipitation[lat_idx, lon_idx] += flipped_arr[i, j] * 2

        # 设置子图
        axes[fig_i].set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
        axes[fig_i].set_title(title_list[fig_i], fontsize=18, y=1.02)
        axes[fig_i].add_feature(cfeature.LAND, zorder=0, edgecolor='black')
        axes[fig_i].add_feature(cfeature.COASTLINE, linewidth=1.5)

        # 添加经纬度网格
        gl = axes[fig_i].gridlines(draw_labels=True, color='gray', linestyle='--', alpha=0.5)
        gl.xlabel_style = {'size': 12}
        gl.ylabel_style = {'size': 12}
        gl.top_labels = False
        gl.right_labels = False

        # 绘制降雨数据
        #大于180的要处理
        if not only_track:
            lon_grid = np.where(lon_grid > 180, lon_grid - 360, lon_grid)
            lon_grid_2d, lat_grid_2d = np.meshgrid(lon_grid, lat_grid)
            contour = axes[fig_i].contourf(lon_grid_2d, lat_grid_2d, accumulated_precipitation,
                                           transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, alpha=1)
            if fig_i == 0:
                contour_bar = copy.copy(contour)

        # 绘制台风路径
        # 大于180的要处理
        typhoon_path_lon = np.where(typhoon_path_lon > 180, typhoon_path_lon - 360, typhoon_path_lon)
        path_color = 'black' if fig_i == 0 else 'red'
        axes[fig_i].scatter(typhoon_path_lon, typhoon_path_lat, color=path_color, s=10,alpha=0.5)
        axes[fig_i].plot(typhoon_path_lon, typhoon_path_lat, color=path_color, linewidth=3,alpha=0.5)
        legend_elements = [Line2D([0], [0], color=path_color, lw=3, marker='o', markersize=5,label=track_predictor[fig_i])]
        axes[fig_i].legend(handles=legend_elements)
        # axes[fig_i].legend()

    # 调整子图和颜色条的位置
    plt.subplots_adjust(left=0.08, right=0.95, top=0.9, bottom=0.20, wspace=0.15)
    cbar_ax = fig.add_axes([0.15, 0.12, 0.7, 0.03])
    if not only_track:
        cbar = fig.colorbar(contour_bar, cax=cbar_ax, orientation='horizontal')
        cbar.set_label('Accumulated Precipitation (mm)', fontsize=15)
        cbar.ax.tick_params(labelsize=12)

    # 保存并展示
    os.makedirs('Accumulated_Precipitation_3_12_track', exist_ok=True)
    plt.savefig(os.path.join('Accumulated_Precipitation_3_12_track', file_name + '.png'), bbox_inches='tight')
    # plt.show()
    plt.close()


def get_resource_data():
    rain_track_data = np.load('rain2track_index.npy',allow_pickle=True)
    rain_all = np.load('rainfall_prediction/gt_all.npy')
    rain_all_pre = np.load('rainfall_prediction/TCP_prediction_all.npy')

    TCs = {}
    for rain_i, rain_track_one in enumerate(rain_track_data):
        if rain_track_one is None:
            continue
        TCs_key = str(rain_track_one['year'])+'_'+rain_track_one['area']+'_'+rain_track_one['name']
        if TCs_key not in TCs.keys():
            TCs[TCs_key]=[]

        TCs[TCs_key].append(rain_track_one)

    for tc_i,TC in enumerate(TCs):
        # if tc_i>0:
        #     continue

        track = []
        rainfall= []
        track_pre = []
        rainfall_pre = []
        for rain_i, rain_track_one in enumerate(TCs[TC]):
            if rain_track_one is None:
                continue

            # if rain_track_one['name'] != 'BERGUITTA' or 'location' not in rain_track_one.keys():
            #     continue
            if 'location' not in rain_track_one.keys():
                continue
            # print(rain_track_one['location'])
            track.append(rain_track_one['location'])
            rainfall.append(rain_all[rain_i-1,0])

            track_pre.append(rain_track_one['future_track_pre'][1])
            rainfall_pre.append(rain_all_pre[rain_i, 1])

        track = np.array(track[1:])
        rainfall = rainfall[:-1]
        # show_accumulate_rainfall(track,rainfall_data=rainfall)

        track_pre = np.array(track_pre[:-1])
        rainfall_pre = rainfall_pre[:-1]
        # show_accumulate_rainfall(track_pre, rainfall_data=rainfall_pre)

        track_list = [track,track_pre]
        rainfall_list = [rainfall,rainfall_pre]
        # track_list.append(track)
        # track_list.append(track_pre)
        # rainfall_list.append(rainfall)
        # rainfall_list.append(rainfall_pre)
        title_list = [rain_track_one['name']+' Ground Truth','TCP-Diffusion']
        print(TC,len(track_list[0]))
        if 'BUD' in TC:
            print('xx')
        if len(track_list[0])>5:
            show_accumulate_rainfall_all(track_list, rainfall_data_list=rainfall_list,title_list=title_list,file_name=TC)

def get_resource_data_4EC(time=6,only_track=False):
    step = time//3
    rain_track_data = np.load('rain2track_index_EC.npy',allow_pickle=True)
    rain_all = np.load('rainfall_prediction/gt_all.npy')
    rain_all_pre = np.load('rainfall_prediction/TCP_prediction_all.npy')
    rain_all_pre_EC = np.load('rainfall_prediction/EC_prediction_all.npy')

    TCs = {}
    for rain_i, rain_track_one in enumerate(rain_track_data):
        if rain_track_one is None:
            continue
        TCs_key = str(rain_track_one['year'])+'_'+rain_track_one['area']+'_'+rain_track_one['name']
        if TCs_key not in TCs.keys():
            TCs[TCs_key]=[]
        rain_track_one['id_order']=rain_i
        TCs[TCs_key].append(rain_track_one)

    for tc_i,TC in enumerate(TCs):
        # if tc_i>0:
        #     continue

        track = []
        rainfall= []
        track_pre = []
        rainfall_pre = []
        track_EC = []
        rainfall_EC = []
        for TC_one, rain_track_one in enumerate(TCs[TC]):
            if rain_track_one is None:
                continue
            id_order = rain_track_one['id_order']
            # if rain_track_one['name'] != 'BERGUITTA' or 'location' not in rain_track_one.keys():
            #     continue
            if 'location' not in rain_track_one.keys():
                continue
            # print(rain_track_one['location'])
            track.append(rain_track_one['location'])
            rainfall.append(rain_all[id_order-1,0])

            track_pre.append(rain_track_one['future_track_pre'][step-1])
            rainfall_pre.append(rain_all_pre[id_order, step-1])
            if 'future_track_pre_EC' in rain_track_one.keys() and rain_track_one['future_track_pre_EC'].shape == (4,2):
                track_EC.append(rain_track_one['future_track_pre_EC'][step-1])
                rainfall_EC.append(rain_all_pre_EC[id_order, step-1])

        track = np.array(track[1:])
        rainfall = rainfall[1:]
        # show_accumulate_rainfall(track,rainfall_data=rainfall)

        track_pre = np.array(track_pre[:-1])
        rainfall_pre = rainfall_pre[:-1]

        track_EC = np.array(track_EC[:-1])
        rainfall_EC = rainfall_EC[:-1]
        # show_accumulate_rainfall(track_pre, rainfall_data=rainfall_pre)

        track_list = [track,track_pre,track_EC]
        rainfall_list = [rainfall,rainfall_pre,rainfall_EC]
        # track_list.append(track)
        # track_list.append(track_pre)
        # rainfall_list.append(rainfall)
        # rainfall_list.append(rainfall_pre)
        title_list = [rain_track_one['name']+' Ground Truth','TCP-Diffusion','ECMWF']
        track_predictor = ['Ground-Truth','MGTCF','ECMWF']
        print(TC,len(track_list[0]))
        if 'BUD' in TC:
            print('xx')
        if len(track_list[0])>5:
            show_accumulate_rainfall_all(track_list, rainfall_data_list=rainfall_list,title_list=title_list,file_name=TC,track_predictor=track_predictor,only_track=only_track)

def show_one_case(track=None,rainfall_data=None,file_name=None):
    '''
        检查降雨的分布   上面是高纬度，下面是低纬度？？？？？？？？
        :param track: 台风轨迹 shape=[8,2],前4真实，后4预测
        :param rainfall_data: 台风降雨 shape=[4,h,w]

        :return:保存前4真实路径图，前4+后4路径图，降雨图，降雨图映射到后4的路径图
        '''
    # 假设我们有台风路径的经纬度和降雨数据（以示例数据代替）
    # 台风路径经纬度
    cmap, norm = colormap()
    typhoon_path_lon = track[:, 0]
    typhoon_path_lat = track[:, 1]

    #   这里的经度不能大于180  大于180就变成负的了
    lon_min, lon_max, lat_min, lat_max = show_range(typhoon_path_lon, typhoon_path_lat)
    grid_resolution = 10 / 64  # 设置网格分辨率（单位：度）
    lon_grid = np.arange(lon_min, lon_max, grid_resolution)
    lat_grid = np.arange(lat_min, lat_max, grid_resolution)
    accumulated_precipitation = np.zeros((len(lat_grid), len(lon_grid)))

# 保存降雨信息
    os.makedirs(os.path.join(BASE_SAVE_DIR, 'rainfall'), exist_ok=True)
    for rain_i in range(np.shape(rainfall_data)[0]):
        cmap_single,norm_single = colormap_single()
        plt.imshow(rainfall_data[rain_i],cmap=cmap_single, norm=norm_single)
        cbar = plt.colorbar(orientation='vertical', label="Accumulated Precipitation (mm/3h)")
        cbar.set_label("Accumulated Precipitation (mm/3h)", fontsize=14)
        # plt.xticks([])  # 隐藏x轴刻度
        # plt.yticks([])  # 隐藏y轴刻度
        plt.axis('off')
        plt.savefig(os.path.join(BASE_SAVE_DIR, 'rainfall',file_name+'_bar'+str(rain_i) + '.png'),bbox_inches='tight', dpi=300)
        plt.close()


    # 累积降雨数据
    for step in range(4,8):
        # if step >0:
        #     continue
        # 获取每个 step 的降雨数据及其覆盖的经纬度范围
        step_lon = np.linspace(typhoon_path_lon[step] - 5, typhoon_path_lon[step] + 5, rainfall_data[step-4].shape[1])
        step_lat = np.linspace(typhoon_path_lat[step] - 5, typhoon_path_lat[step] + 5, rainfall_data[step-4].shape[0])

        # 找到大网格中对应的索引范围
        lon_indices = np.searchsorted(lon_grid, step_lon)
        lat_indices = np.searchsorted(lat_grid, step_lat)

        # 将降雨数据累加到对应位置
        flipped_arr = np.flip(rainfall_data[step-4], axis=0)
        for i, lat_idx in enumerate(lat_indices):
            for j, lon_idx in enumerate(lon_indices):
                # if accumulated_precipitation[lat_idx, lon_idx]<flipped_arr[i, j]:
                #     accumulated_precipitation[lat_idx, lon_idx] = flipped_arr[i, j]
                accumulated_precipitation[lat_idx, lon_idx] += flipped_arr[i, j] * 2

    # 创建地图
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())  # 设置地图范围
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False  # 不在顶部显示纬度标签
    gl.right_labels = False  # 不在右侧显示经度标签
    # 添加地图特征
    ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)

    # 绘制降雨数据
    # for step in range(np.shape(typhoon_path_lon)[0]):
    #     if step > 0:
    #         continue
    #     # 降雨数据示例，假设降雨范围为10°x10°
    #     # rainfall_data = np.random.rand(10, 10) * 100  # 随机生成示例降雨数据
    #     rainfall_lon = np.linspace(typhoon_path_lon[step] - 5, typhoon_path_lon[step] + 5, 64)
    #     rainfall_lat = np.linspace(typhoon_path_lat[step] - 5, typhoon_path_lat[step] + 5, 64)
    #     lon_grid, lat_grid = np.meshgrid(rainfall_lon, rainfall_lat)
    #     ax.contourf(lon_grid, lat_grid, np.flip(rainfall_data[step], axis=0), transform=ccrs.PlateCarree(), cmap=cmap, norm=norm, alpha=0.7)

    lon_grid_2d, lat_grid_2d = np.meshgrid(lon_grid, lat_grid)
    contour = ax.contourf(lon_grid_2d, lat_grid_2d, accumulated_precipitation, transform=ccrs.PlateCarree(),
                          cmap=cmap, norm=norm, alpha=0.7)
    cbar = plt.colorbar(contour, ax=ax, orientation='vertical', label="Accumulated Precipitation (mm/12h)")
    cbar.set_label("Accumulated Precipitation (mm/12h)", fontsize=14)

    # 绘制台风路径
    # ax.plot(typhoon_path_lon, typhoon_path_lat, color='black', linewidth=2, label="Typhoon Path")
    ax.scatter(typhoon_path_lon[:4], typhoon_path_lat[:4], color='red', s=30, label="Historical TC Track")  # 标记台风中心点
    ax.scatter(typhoon_path_lon[4:], typhoon_path_lat[4:], color='green', s=30, label="Predicted TC Track")  # 标记台风中心点

    # 添加标题和图例
    plt.title("TC Track and Predicted Precipitation",fontsize=16)
    plt.legend(fontsize=12)

    # plt.show()
    # 保存并展示
    # os.makedirs('problem_identity_cases', exist_ok=True)
    os.makedirs(BASE_SAVE_DIR, exist_ok=True)
    plt.savefig(os.path.join(BASE_SAVE_DIR, file_name + '.png'), bbox_inches='tight', dpi=300)
    # plt.show()
    plt.close()

    # 保存history data
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())  # 设置地图范围
    # gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    # gl.top_labels = False  # 不在顶部显示纬度标签
    # gl.right_labels = False  # 不在右侧显示经度标签
    # 添加地图特征
    ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    os.makedirs(os.path.join(BASE_SAVE_DIR, 'gt_track'), exist_ok=True)
    ax.scatter(typhoon_path_lon[:4], typhoon_path_lat[:4], color='red', s=30, label="Historical TC Track")  # 标记台风中心点
    plt.legend()
    plt.savefig(os.path.join(BASE_SAVE_DIR, 'gt_track', file_name + '.png'),
                bbox_inches='tight', dpi=300)
    plt.close()

    # 保存alltrack
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())  # 设置地图范围
    # gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    # gl.top_labels = False  # 不在顶部显示纬度标签
    # gl.right_labels = False  # 不在右侧显示经度标签
    # 添加地图特征
    ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    os.makedirs(os.path.join(BASE_SAVE_DIR, 'alltrack'), exist_ok=True)
    ax.scatter(typhoon_path_lon[:4], typhoon_path_lat[:4], color='red', s=30, label="Historical TC Track")  # 标记台风中心点
    ax.scatter(typhoon_path_lon[4:], typhoon_path_lat[4:], color='green', s=30, label="Predicted TC Track")  # 标记台风中心点
    plt.legend()
    plt.savefig(os.path.join(BASE_SAVE_DIR, 'alltrack', file_name + '.png'),
                bbox_inches='tight', dpi=300)
    plt.close()



def get_resource_data_problem_difinition():
    rain_track_data = np.load('rain2track_index.npy', allow_pickle=True)
    rain_all = np.load('rainfall_prediction/gt_all.npy')
    rain_all_pre = np.load('rainfall_prediction/TCP_prediction_all.npy')
    case_list = ['2018_SI_CILIDA2018122106',
                 '2019_SI_LORNA2019042600',
                 '2019_WP_LINGLING2019090418',
                 '2019_WP_LINGLING2019090512',
                 '2019_NA_HUMBERTO2019091418',
                 '2019_WP_MITAG2019093000',
                 '2019_WP_KALMAEGI2019111712'
                 '2020_NA_HANNA2020072418',
                 '2020_NA_ZETA2020102700']
    TCs = {}
    for rain_i, rain_track_one in enumerate(rain_track_data):
        if rain_track_one is None:
            continue
        TCs_key = str(rain_track_one['year']) + '_' + rain_track_one['area'] + '_' + rain_track_one['name']
        if TCs_key not in TCs.keys():
            TCs[TCs_key] = []

        TCs[TCs_key].append(rain_track_one)

    for tc_i, TC in enumerate(TCs):
        # if tc_i>0:
        #     continue

        track = []
        rainfall = []
        track_pre = []
        rainfall_pre = []
        for rain_i, rain_track_one in enumerate(TCs[TC]):
            if rain_track_one is None:
                continue

            # if rain_track_one['name'] != 'BERGUITTA' or 'location' not in rain_track_one.keys():
            #     continue
            if 'location' not in rain_track_one.keys():
                continue
            # print(rain_track_one['location'])
            # track.append(rain_track_one['location'])
            yyyymmddhh = f"{int(rain_track_one['year']):04d}{int(rain_track_one['month']):02d}{int(rain_track_one['day']):02d}{int(rain_track_one['hour']):02d}"


            gt_track = rain_track_one['future_track_gt']
            gt_rainfall = rain_all[rain_i - 1]
            if TC+yyyymmddhh in case_list:
                show_one_case(gt_track,gt_rainfall,TC+yyyymmddhh)




if __name__ == '__main__':
    # get_resource_data()
    # get_resource_data_4EC(6,only_track=True)
    # show_accumulate_rainfall()
    # get_resource_data_problem_difinition()
    show_one_case()

