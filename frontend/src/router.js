import { createRouter, createWebHistory } from 'vue-router'
import { userResource } from '@/stores/user'
import { sessionStore } from '@/stores/session'
import { useLoadingStore } from "@/stores/loading"; 

const routes = [
  {
    path: '/',
    redirect: { name: 'Leads' },
    name: 'Home',
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: () => import('@/pages/MobileNotification.vue'),
  },
  {
    alias: '/leads',
    path: '/leads/view/:viewType?',
    name: 'Leads',
    component: () => import('@/pages/Leads.vue'),
  },
  {
    path: '/leads/:leadId',
    name: 'Lead',
    component: () => import(`@/pages/${handleMobileView('Lead')}.vue`),
    props: true,
  },
  {
    alias: '/deals',
    path: '/deals/view/:viewType?',
    name: 'Deals',
    component: () => import('@/pages/Deals.vue'),
  },
  {
    path: '/deals/:name',
    name: 'Deal',
    component: () => import(`@/pages/${handleMobileView('Deal')}.vue`),
    props: true,
  },
  {
    alias: '/notes',
    path: '/notes/view/:viewType?',
    name: 'Notes',
    component: () => import('@/pages/Notes.vue'),
  },
  {
    alias: '/tasks',
    path: '/tasks/view/:viewType?',
    name: 'Tasks',
    component: () => import('@/pages/Tasks.vue'),
  },
  {
    alias: '/contacts',
    path: '/contacts/view/:viewType?',
    name: 'Contacts',
    component: () => import('@/pages/Contacts.vue'),
  },
  {
    path: '/contacts/:name',
    name: 'Contact',
    component: () => import(`@/pages/${handleMobileView('Contact')}.vue`),
    props: true,
  },
  {
    alias: '/organizations',
    path: '/organizations/view/:viewType?',
    name: 'Organizations',
    component: () => import('@/pages/Organizations.vue'),
  },
  {
    path: '/organizations/:name',
    name: 'Organization',
    component: () => import(`@/pages/${handleMobileView('Organization')}.vue`),
    props: true,
  },
  {
    alias: '/call-logs',
    path: '/call-logs/view/:viewType?',
    name: 'Call Logs',
    component: () => import('@/pages/CallLogs.vue'),
  },
  {
    alias: '/email-templates',
    path: '/email-templates/view/:viewType?',
    name: 'Email Templates',
    component: () => import('@/pages/EmailTemplates.vue'),
  },
  {
    path: '/email-templates/:emailTemplateId',
    name: 'Email Template',
    component: () => import('@/pages/EmailTemplate.vue'),
    props: true,
  },
  {
    path: '/financial-discovery/',
    name: 'FDList',
    component: () => import('@/pages/FD/FinancialDiscoveryList.vue'),
    meta: {
      title: "FD List",
      isAuth: true
    }
  },
  {
    path: '/financial-discovery/create',
    name: 'CreateFD',
    component: () => import('@/pages/FD/FinancialDiscovery.vue'),
  },
  {
    path: '/financial-discovery/:id',
    name: 'FDDetails',
    component: () => import('@/pages/FD/FinancialDiscoveryDetails.vue'),
    meta: {
      title: "FD Details",
      isAuth: true
    }
  },
  {
    path: '/financial-discovery/edit/:id',
    name: 'EditFD',
    component: () => import('@/pages/FD/EditFinancialDiscovery.vue'),
    meta: {
      title: "Edit FD",
      isAuth: true
    }
  },
  {
    path: '/:invalidpath',
    name: 'Invalid Page',
    component: () => import('@/pages/InvalidPage.vue'),
  },
]

const handleMobileView = (componentName) => {
  return window.innerWidth < 768 ? `Mobile${componentName}` : componentName
}

let router = createRouter({
  history: createWebHistory('/crm'),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const loadingStore = useLoadingStore();
  loadingStore.setLoading(true); 
  
  const { isLoggedIn } = sessionStore()

  isLoggedIn && (await userResource.promise)

  if (to.name === 'Home' && isLoggedIn) {
    next({ name: 'Leads' })
  } else if (!isLoggedIn) {
    window.location.href = '/login?redirect-to=/crm'
  } else if (to.matched.length === 0) {
    next({ name: 'Invalid Page' })
  } else if (['Deal', 'Lead'].includes(to.name) && !to.hash) {
    let storageKey = to.name === 'Deal' ? 'lastDealTab' : 'lastLeadTab'
    const activeTab = localStorage.getItem(storageKey) || 'activity'
    const hash = '#' + activeTab
    next({ ...to, hash })
  } else {
    next()
  }
})

export default router
