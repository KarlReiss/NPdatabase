package cn.npdb.service.impl;

import cn.npdb.entity.Bioactivity;
import cn.npdb.mapper.BioactivityMapper;
import cn.npdb.service.BioactivityService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class BioactivityServiceImpl extends ServiceImpl<BioactivityMapper, Bioactivity> implements BioactivityService {
}
