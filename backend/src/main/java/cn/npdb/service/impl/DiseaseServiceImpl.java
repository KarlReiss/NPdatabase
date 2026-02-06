package cn.npdb.service.impl;

import cn.npdb.entity.Disease;
import cn.npdb.mapper.DiseaseMapper;
import cn.npdb.service.DiseaseService;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import org.springframework.stereotype.Service;

@Service
public class DiseaseServiceImpl extends ServiceImpl<DiseaseMapper, Disease> implements DiseaseService {
    @Override
    public Page<Disease> listPage(long page, long pageSize, String q, String category) {
        Page<Disease> mpPage = new Page<>(page, pageSize);
        return baseMapper.selectListPage(mpPage, q, category);
    }
}
