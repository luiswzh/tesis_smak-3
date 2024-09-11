# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 13:34:14 2024

@author: luisw

Calculate circular stats for pandas series
"""
import scipy.stats as stats

def mean(srgroup, crange):
    return srgroup.apply(lambda x: stats.circmean(x,high=crange[1],low=crange[0]))

def std(srgroup, crange):
    return srgroup.apply(lambda x: stats.circstd(x,high=crange[1],low=crange[0]))