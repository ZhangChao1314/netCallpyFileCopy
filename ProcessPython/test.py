import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import symfit as sf
import sys



# Generate example data
# excel 3列 第一列P   第二列V  第三列温度  
path1 = r'D:\\C#\\netCallpyFileCopy\\ProcessPython\\bin\\Debug\\test.xlsx'


# 读取文件，并按照最后一列T的从小到大的顺序排列
def pdread(filename):
    df1=pd.read_excel(filename)    
    height1,width1 = df1.shape
    matrix1 = np.zeros((height1,width1))
    for i in range(0,height1):
        for j in range(0,width1):
            matrix1[i][j] = df1.iloc[i,j]
    matrix1 = matrix1[np.lexsort(matrix1.T)]
    x0 = matrix1[:,0]
    x0 = np.array(x0)
    y0 = matrix1[:,1]
    y0 = np.array(y0)
    T0 = matrix1[:,2]
    T0 = np.array(T0)
    return [x0,y0,T0]

# 识别有几个温度文件，并返回温度和每个温度长度
def uniquedataandcount(data):
    data = sorted(data)
    #print(data)
    unique_data = np.unique(data)
    #print(unique_data)
    resdata = []
    for ii in unique_data:
        resdata.append(data.count(ii))
    #print(resdata)
    return unique_data,resdata

# 统计一个数组中，出现target的次数
def mfun(nums,target):
    n=0
    for i in nums:
        if i == target:
            n+=1
    return n

#生成symfit所需要的globalfit的数据集
def cratedaset(x0,y0,T0):
    Tdata,count = uniquedataandcount(T0)
    for ii in range(len(count)):
        if ii==0:
            startindex = 0
            endindex = count[ii]        
        else:
            startindex+=count[ii-1]
            endindex+=count[ii]
        xtemp = x0[startindex:endindex]
        ytemp = y0[startindex:endindex]
        if ii==0:
            xdata = xtemp
            ydata = ytemp
        else:
            #xdata = np.vstack([xdata, xtemp])
            #ydata = np.vstack([ydata, ytemp])
            xdata = np.append(xdata, xtemp)
            ydata = np.append(ydata, ytemp)
    return xdata,ydata,Tdata

#执行global fit
def datasetglobalfit(x0,y0,T0):
    # create dataset_dict
    Tdata,count = uniquedataandcount(T0)
    keysx =['x_{}'.format(i) for i in range(len(count))]
    keysy =['y_{}'.format(i) for i in range(len(count))]
    keys = keysx + keysy
    data_dict ={}
    xdata_dict ={}
    ydata_dict ={}
    
    for ii in range(len(count)):
        if ii==0:
            startindex = 0
            endindex = count[ii]        
        else:
            startindex+=count[ii-1]
            endindex+=count[ii]
        #P unit Kpa
        Ptemp = x0[startindex:endindex]
        Vtemp = y0[startindex:endindex]
        LnP_1000 = np.log(Ptemp * 1000.0)
        V_mmol = Vtemp /22.414
        xdata_dict.update({keysx[ii]: V_mmol})
        ydata_dict.update({keysy[ii]: LnP_1000})
     
    data_dict=dict(xdata_dict,**ydata_dict)   

    # independent variables
    xs = sf.variables(', '.join('x_{}'.format(i) for i in range(len(count))))
    # dependent variables
    ys = sf.variables(', '.join('y_{}'.format(i) for i in range(len(count))))
    #拟合代码删除掉了哈

    
    return xdata_dict,ydata_dict, keysx, keysy

def virial(path):    
    x0,y0,T0= pdread(path)

    #plot csatter origin data
    comboY = y0
    comboX = x0

    # get T and array count
    Tdata,count = uniquedataandcount(T0)

    # do fit
    xdata_dict,ydata_dict, keysx, keysy= datasetglobalfit(x0,y0,T0)
    

    #创建图形
    plt.figure(1)
    plt.rcParams['figure.figsize'] = (15.0, 10.0)
    #同一画布
    plt.subplot(1,2,1)
    for i in range(len(count)):
        plt.plot(xdata_dict[keysx[i]], ydata_dict[keysy[i]], 'D',label='{} K_Origin'.format(Tdata[i])) # plot the raw dataf
        #plt.plot(xdata_dict[keysx[i]],y_r[i],label='{} K_Fit'.format(Tdata[i]))
    plt.legend()
    a0, a1, a2, a3, a4, a5, a6, a7 = [0,1, 2, 3, 4, 5, 6, 7]
    plt.show()
    return a0, a1, a2, a3, a4, a5, a6, a7



#if __name__ == '__mmain__':
#    print(virial(sys.argv[1]))


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description="WAVE")
    #parser.add_argument('--path', dest='path', type=str)
    #args = parser.parse_args()
    if len(sys.argv) == 2:
        path = sys.argv[1]
        print(virial(path))
    else:
        virial(path1)
        

    
    
        
    

