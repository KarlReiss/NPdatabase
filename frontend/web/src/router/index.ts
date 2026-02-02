import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '@/pages/Home.vue';
import NaturalProductList from '@/pages/NaturalProductList.vue';
import NaturalProductDetail from '@/pages/NaturalProductDetail.vue';
import TargetList from '@/pages/TargetList.vue';
import TargetDetail from '@/pages/TargetDetail.vue';
import BioResourceList from '@/pages/BioResourceList.vue';
import BioResourceDetail from '@/pages/BioResourceDetail.vue';
import PrescriptionList from '@/pages/PrescriptionList.vue';
import PrescriptionDetail from '@/pages/PrescriptionDetail.vue';
import DiseaseList from '@/pages/DiseaseList.vue';
import DiseaseDetail from '@/pages/DiseaseDetail.vue';
import TopicList from '@/pages/TopicList.vue';
import TopicDetail from '@/pages/TopicDetail.vue';

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/natural-products', name: 'natural-product-list', component: NaturalProductList },
    { path: '/natural-products/:id', name: 'natural-product-detail', component: NaturalProductDetail, props: true },
    { path: '/targets', name: 'target-list', component: TargetList },
    { path: '/targets/:id', name: 'target-detail', component: TargetDetail, props: true },
    { path: '/bio-resources', name: 'bio-resource-list', component: BioResourceList },
    { path: '/bio-resources/:id', name: 'bio-resource-detail', component: BioResourceDetail, props: true },
    { path: '/prescriptions', name: 'prescription-list', component: PrescriptionList },
    { path: '/prescriptions/:id', name: 'prescription-detail', component: PrescriptionDetail, props: true },
    { path: '/diseases', name: 'disease-list', component: DiseaseList },
    { path: '/diseases/:id', name: 'disease-detail', component: DiseaseDetail, props: true },
    { path: '/topics', name: 'topic-list', component: TopicList },
    { path: '/topics/:id', name: 'topic-detail', component: TopicDetail, props: true },
    // Legacy redirects for backward compatibility
    { path: '/compounds', redirect: '/natural-products' },
    { path: '/compounds/:id', redirect: (to) => `/natural-products/${to.params.id}` },
    { path: '/resources', redirect: '/bio-resources' },
    { path: '/resources/:id', redirect: (to) => `/bio-resources/${to.params.id}` },
    { path: '/list', redirect: '/natural-products' },
    { path: '/detail/:id', redirect: (to) => `/natural-products/${to.params.id}` },
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;
