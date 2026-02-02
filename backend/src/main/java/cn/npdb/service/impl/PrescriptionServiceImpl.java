package cn.npdb.service.impl;

import cn.npdb.entity.Prescription;
import cn.npdb.mapper.PrescriptionMapper;
import cn.npdb.service.PrescriptionService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class PrescriptionServiceImpl extends ServiceImpl<PrescriptionMapper, Prescription> implements PrescriptionService {
}
