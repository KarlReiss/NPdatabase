package cn.npdb.service.impl;

import cn.npdb.entity.PrescriptionResource;
import cn.npdb.mapper.PrescriptionResourceMapper;
import cn.npdb.service.PrescriptionResourceService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class PrescriptionResourceServiceImpl extends ServiceImpl<PrescriptionResourceMapper, PrescriptionResource> implements PrescriptionResourceService {
}
