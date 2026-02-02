package cn.npdb.service.impl;

import cn.npdb.entity.Toxicity;
import cn.npdb.mapper.ToxicityMapper;
import cn.npdb.service.ToxicityService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class ToxicityServiceImpl extends ServiceImpl<ToxicityMapper, Toxicity> implements ToxicityService {
}
