package cn.npdb.service.impl;

import cn.npdb.entity.BioResource;
import cn.npdb.mapper.BioResourceMapper;
import cn.npdb.service.BioResourceService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class BioResourceServiceImpl extends ServiceImpl<BioResourceMapper, BioResource> implements BioResourceService {
}
