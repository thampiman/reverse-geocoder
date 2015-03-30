##
# Author: Ajay Thampi
# Code extended from http://folk.uio.no/sturlamo/python/multiprocessing-tutorial.pdf
##
import numpy as np
import scipy
import scipy.spatial
import multiprocessing as mp
import ctypes
import os
import sys
from scipy.spatial import cKDTree

def shmem_as_nparray(shmem_array):
    return np.frombuffer(shmem_array.get_obj())

def _pquery(scheduler,data,ndata,ndim,leafsize,
                x,nx,d,i,k,eps,p,dub,ierr):
    try:
        _data = shmem_as_nparray(data).reshape((ndata,ndim))
        _x = shmem_as_nparray(x).reshape((nx,ndim))
        _d = shmem_as_nparray(d).reshape((nx,k))
        _i = shmem_as_nparray(i).reshape((nx,k))

        kdtree = cKDTree(_data,leafsize=leafsize)

        for s in scheduler:
            d_out,i_out = kdtree.query(_x[s,:],k=k,eps=eps,p=p,distance_upper_bound=dub)
            m_d = d_out.shape[0]
            m_i = i_out.shape[0]
            _d[s,:],_i[s,:] = d_out.reshape(m_d,1),i_out.reshape(m_i,1)
    except:
        ierr.value += 1

def num_cpus():
    try:
        return mp.cpu_count()        
    except NotImplementedError:
        return 2 

class cKDTree_MP(cKDTree):
    def __init__(self,data_list,leafsize=30):
        data = np.array(data_list)
        n,m = data.shape
        self.shmem_data = mp.Array(ctypes.c_double,n*m)

        _data = shmem_as_nparray(self.shmem_data).reshape((n,m))
        _data[:,:] = data

        self._leafsize = leafsize
        super(cKDTree_MP,self).__init__(_data,leafsize=leafsize)

    def pquery(self,x_list,k=1,eps=0,p=2,
               distance_upper_bound=np.inf):
        x = np.array(x_list)
        nx,mx = x.shape
        shmem_x = mp.Array(ctypes.c_double,nx*mx)
        shmem_d = mp.Array(ctypes.c_double,nx*k)
        shmem_i = mp.Array(ctypes.c_double,nx*k)

        _x = shmem_as_nparray(shmem_x).reshape((nx,mx))
        _d = shmem_as_nparray(shmem_d).reshape((nx,k))

        _i = shmem_as_nparray(shmem_i)
        if k != 1:
            _i = _i.reshape((nx,k))

        _x[:,:] = x

        nprocs = num_cpus()
        scheduler = Scheduler(nx,nprocs)

        ierr = mp.Value(ctypes.c_int, 0)

        query_args = (scheduler,
                      self.shmem_data,self.n,self.m,self.leafsize,
                      shmem_x,nx,shmem_d,shmem_i,
                      k,eps,p,distance_upper_bound,
                      ierr
                     )
        pool = [mp.Process(target=_pquery,args=query_args) for n in range(nprocs)]
        for p in pool: p.start()
        for p in pool: p.join()
        if ierr.value != 0:
            raise RuntimeError('%d errors in worker processes' % (ierr.value))

        return _d.copy(),_i.astype(int).copy()

class Scheduler:
    def __init__(self,ndata,nprocs):
        self._ndata = mp.RawValue(ctypes.c_int,ndata)
        self._start = mp.RawValue(ctypes.c_int,0)
        self._lock = mp.Lock()
        min_chunk = ndata // nprocs
        min_chunk = ndata if min_chunk <= 2 else min_chunk
        self._chunk = min_chunk

    def __iter__(self):
        return self

    def next(self): # Python 2 support
        self._lock.acquire()
        ndata = self._ndata.value
        start = self._start.value
        chunk = self._chunk 
        if ndata:
            if chunk > ndata:
                s0 = start
                s1 = start + ndata
                self._ndata.value = 0
            else:
                s0 = start
                s1 = start + chunk
                self._ndata.value = ndata - chunk
                self._start.value = start + chunk
            self._lock.release()
            return slice(s0, s1)
        else:
            self._lock.release()
            raise StopIteration  

    def __next__(self): # Python 3 support
        self._lock.acquire()
        ndata = self._ndata.value
        start = self._start.value
        chunk = self._chunk 
        if ndata:
            if chunk > ndata:
                s0 = start
                s1 = start + ndata
                self._ndata.value = 0
            else:
                s0 = start
                s1 = start + chunk
                self._ndata.value = ndata - chunk
                self._start.value = start + chunk
            self._lock.release()
            return slice(s0, s1)
        else:
            self._lock.release()
            raise StopIteration 
        