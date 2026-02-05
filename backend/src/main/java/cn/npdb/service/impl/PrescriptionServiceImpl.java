package cn.npdb.service.impl;

import cn.npdb.dto.PrescriptionListItem;
import cn.npdb.entity.Prescription;
import cn.npdb.mapper.PrescriptionMapper;
import cn.npdb.service.PrescriptionService;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class PrescriptionServiceImpl extends ServiceImpl<PrescriptionMapper, Prescription> implements PrescriptionService {
    @Override
    public Page<PrescriptionListItem> listPage(Page<?> page, String q) {
        return baseMapper.selectListPage(page, q);
    }
}
