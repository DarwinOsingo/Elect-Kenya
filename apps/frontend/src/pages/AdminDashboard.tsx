import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import API from '../lib/api';
import { AlertCircle, Lock, Plus } from 'lucide-react';

async function verifyAdminAccess(): Promise<boolean> {
  const token = localStorage.getItem('admin_token');
  if (!token) return false;
  try {
    await API.get('/admin/verify', {
      headers: { 'X-API-Key': token },
    });
    return true;
  } catch {
    return false;
  }
}

export default function AdminDashboard() {
  const [token, setToken] = useState(localStorage.getItem('admin_token') || '');
  const [showTokenInput, setShowTokenInput] = useState(!localStorage.getItem('admin_token'));
  const [activeTab, setActiveTab] = useState('candidates');

  const { data: isAdmin, isLoading, refetch } = useQuery({
    queryKey: ['admin-verify'],
    queryFn: verifyAdminAccess,
    enabled: !!token,
  });

  const handleLogin = () => {
    if (token) {
      localStorage.setItem('admin_token', token);
      refetch();
      setShowTokenInput(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('admin_token');
    setToken('');
    setShowTokenInput(true);
  };

  if (!isAdmin && !showTokenInput) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="p-6 bg-destructive/10 border border-destructive rounded-lg flex gap-4">
          <Lock className="w-6 h-6 text-destructive flex-shrink-0" />
          <div>
            <h3 className="font-bold text-destructive mb-2">Authentication Required</h3>
            <p className="text-sm text-muted-foreground mb-4">
              You need to provide a valid API key to access the admin dashboard.
            </p>
            <button
              onClick={() => setShowTokenInput(true)}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition"
            >
              Enter API Key
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (showTokenInput) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <div>
          <h1 className="text-4xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-lg text-muted-foreground">Manage site content and data.</p>
        </div>

        <div className="p-6 border rounded-lg bg-card space-y-4">
          <h2 className="text-xl font-bold">API Key Authentication</h2>
          <input
            type="password"
            placeholder="Enter your API key"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg bg-background"
          />
          <div className="flex gap-2">
            <button
              onClick={handleLogin}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition"
            >
              Login
            </button>
            <button
              onClick={() => {
                setToken('');
                setShowTokenInput(false);
              }}
              className="px-4 py-2 border rounded-lg font-medium hover:bg-muted transition"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAdmin) {
    return (
      <div className="p-6 bg-destructive/10 border border-destructive rounded-lg flex gap-2">
        <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
        <div>
          <h3 className="font-medium text-destructive">Invalid API Key</h3>
          <p className="text-sm text-muted-foreground">The API key you provided is not valid.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold mb-2">Admin Dashboard</h1>
          <p className="text-lg text-muted-foreground">Manage candidates, counties, and site content.</p>
        </div>
        <button
          onClick={handleLogout}
          className="px-4 py-2 border rounded-lg font-medium hover:bg-muted transition"
        >
          Logout
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b">
        {['candidates', 'counties', 'issues', 'vote-buying'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 font-medium border-b-2 transition-colors ${
              activeTab === tab
                ? 'border-primary text-primary'
                : 'border-transparent text-muted-foreground hover:text-foreground'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Content Area */}
      <div className="space-y-4">
        {activeTab === 'candidates' && (
          <div className="space-y-4">
            <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition">
              <Plus className="w-4 h-4" />
              Add Candidate
            </button>
            <div className="p-6 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">
                Candidate management forms will be displayed here. Currently in stub mode for MVP.
              </p>
            </div>
          </div>
        )}

        {activeTab === 'counties' && (
          <div className="space-y-4">
            <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition">
              <Plus className="w-4 h-4" />
              Add County
            </button>
            <div className="p-6 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">
                County management forms will be displayed here. Currently in stub mode for MVP.
              </p>
            </div>
          </div>
        )}

        {activeTab === 'issues' && (
          <div className="space-y-4">
            <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition">
              <Plus className="w-4 h-4" />
              Add Issue
            </button>
            <div className="p-6 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">
                Issue management forms will be displayed here. Currently in stub mode for MVP.
              </p>
            </div>
          </div>
        )}

        {activeTab === 'vote-buying' && (
          <div className="space-y-4">
            <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition">
              <Plus className="w-4 h-4" />
              Add Fact
            </button>
            <div className="p-6 bg-muted rounded-lg">
              <p className="text-sm text-muted-foreground">
                Vote-buying information management will be displayed here. Currently in stub mode for MVP.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
