import {
  RootRoute,
  Router,
  Route,
  Outlet,
  useRouterState,
  Link,
  Navigate,
} from '@tanstack/react-router';
import { ThemeProvider } from './lib/theme';
import { useTheme } from './lib/theme';
import Layout from './components/Layout';
import HomePage from './pages/Home';
import CandidatesPage from './pages/Candidates';
import CandidateDetailPage from './pages/CandidateDetail';
import IssuesPage from './pages/Issues';
import VoteBuyingPage from './pages/VoteBuying';
import WhatCouldHaveBeenPage from './pages/WhatCouldHaveBeen';
import CountiesPage from './pages/Counties';
import CountyDetailPage from './pages/CountyDetail';
import AdminDashboard from './pages/AdminDashboard';
import AboutPage from './pages/About';
import ResourcesPage from './pages/Resources';

// Root Layout Component
function RootComponent() {
  return (
    <ThemeProvider>
      <Layout>
        <Outlet />
      </Layout>
    </ThemeProvider>
  );
}

// Create routes
const rootRoute = new RootRoute({
  component: RootComponent,
});

const indexRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/',
  component: HomePage,
});

const candidatesRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/candidates',
  component: CandidatesPage,
});

const candidateDetailRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/candidates/$slug',
  component: CandidateDetailPage,
});

const issuesRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/issues',
  component: IssuesPage,
});

const voteBuyingRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/vote-buying',
  component: VoteBuyingPage,
});

const whatCouldHaveBeenRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/what-could-have-been',
  component: WhatCouldHaveBeenPage,
});

const countiesRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/counties',
  component: CountiesPage,
});

const countyDetailRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/counties/$name',
  component: CountyDetailPage,
});

const aboutRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/about',
  component: AboutPage,
});

const resourcesRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/resources',
  component: ResourcesPage,
});

const adminRoute = new Route({
  getParentRoute: () => rootRoute,
  path: '/admin',
  component: AdminDashboard,
});

// Create route tree
const routeTree = rootRoute.addChildren([
  indexRoute,
  candidatesRoute,
  candidateDetailRoute,
  issuesRoute,
  voteBuyingRoute,
  whatCouldHaveBeenRoute,
  countiesRoute,
  countyDetailRoute,
  aboutRoute,
  resourcesRoute,
  adminRoute,
]);

// Create router
const router = new Router({ routeTree });

// Register router
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}

export default router;
