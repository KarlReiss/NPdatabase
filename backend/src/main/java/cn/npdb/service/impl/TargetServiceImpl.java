package cn.npdb.service.impl;

import cn.npdb.entity.Target;
import cn.npdb.mapper.TargetMapper;
import cn.npdb.service.TargetService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class TargetServiceImpl extends ServiceImpl<TargetMapper, Target> implements TargetService {
}
