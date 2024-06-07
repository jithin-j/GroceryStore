import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { getUserRole, isAuthenticated } from '../utils/auth'

const USER_ROLES = {
  ADMIN: 'admin',
  MANAGER: 'store manager',
  USER: 'user',
};

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/SignUpView.vue')
    },
    {
      path: '/manager/signup',
      name: 'manager-signup',
      component: () => import('../views/ManagerSignUpView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: () => import('../views/AdminLoginView.vue')
    },
    {
      path: '/manager/login',
      name: 'manager-login',
      component: () => import('../views/ManagerLoginView.vue')
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/AdminDashboardView.vue'),
      meta: { requiredRole: USER_ROLES.ADMIN },
      beforeEnter: guardRouteAccess,
    },
    {
      path: '/section/add',
      name: 'add-section',
      component: () => import('../views/AddSectionView.vue'),
      meta: { requiredRole: USER_ROLES.ADMIN },
      beforeEnter: guardRouteAccess,
    },
    {
      path: '/sections',
      name: 'view-sections',
      component: () => import('../views/ViewSectionsView.vue'),
      meta: { requiredRole: USER_ROLES.ADMIN },
      beforeEnter: guardRouteAccess,
    },
    {
    path: '/product/add',
    name: 'product-add',
    component: () => import('../views/AddProductView.vue'),
    meta: { requiredRole: USER_ROLES.MANAGER },
    beforeEnter: guardRouteAccess,
    },
    {
      path: '/manager/dashboard',
      name: 'manager-dashboard',
      component: () => import('../views/ManagerDashboardView.vue'),
      meta: { requiredRole: USER_ROLES.MANAGER },
      beforeEnter: guardRouteAccess,
    },
    {
      path: '/edit/:productId',
      name: 'edit-product',
      component: () => import('../views/EditProductView.vue'),
      meta: { requiredRole: USER_ROLES.MANAGER },
      beforeEnter: guardRouteAccess,
    },
    {
      path: '/edit-section/:sectionId',
      name: 'edit-section',
      component: () => import('../views/EditSectionView.vue'),
      meta: { requiredRole: USER_ROLES.ADMIN },
      beforeEnter: guardRouteAccess,
    },
    {
      path: '/edit-section-request/:sectionId',
      name: 'edit-section-request',
      component: () => import('../views/ManagerEditSectionView.vue'),
      meta: { requiredRole: USER_ROLES.MANAGER },
      beforeEnter: guardRouteAccess,
    },
    {
      path: '/section-requests',
      name: 'section-requests',
      component: () => import('../views/SectionRequestsView.vue'),
      meta: { requiredRole: USER_ROLES.ADMIN },
      beforeEnter: guardRouteAccess,
    },
    {
      path: '/request/section',
      name: 'request-section',
      component: () => import('../views/ManagerAddSectionView.vue'),
      meta: { requiredRole: USER_ROLES.MANAGER },
      beforeEnter: guardRouteAccess,
    },
    {
      path: '/dashboard',
      name: 'user dashboard',
      component: () => import('../views/UserDashboardView.vue'),
      meta: { requiredRole: USER_ROLES.USER },
      beforeEnter: guardRouteAccess,
    },
    {
      path: '/order-history',
      name: 'order history',
      component: () => import('../views/UserOrderHistoryView.vue'),
      meta: { requiredRole: USER_ROLES.USER },
      beforeEnter: guardRouteAccess,
    },
  ]
});

function guardRouteAccess(to, from, next) {
  const requiredRole = to.meta.requiredRole;

  // Check if the user is authenticated and has the required role
  if (isAuthenticated() && getUserRole() === requiredRole) {
    // User is authenticated and has the required role, allow access
    next();
  } else {
    // User is not authenticated or doesn't have the required role, redirect to login or another page
    // For example, redirect to the home page
    next({ name: 'home' });
  }
}

export default router
