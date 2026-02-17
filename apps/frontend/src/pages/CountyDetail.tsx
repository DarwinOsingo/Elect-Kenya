import { useParams } from '@tanstack/react-router';
import { useQuery } from '@tanstack/react-query';
import API from '../lib/api';
import { County } from '@elect/shared';
import { Skeleton } from '../components/ui/Skeleton';
import { AlertCircle } from 'lucide-react';

async function fetchCounty(name: string): Promise<County> {
  const { data } = await API.get(`/counties/${name}`);
  return data;
}

export default function CountyDetailPage() {
  const { name } = useParams({ from: '/counties/$name' });
  const { data: county, isLoading, error } = useQuery({
    queryKey: ['county', name],
    queryFn: () => fetchCounty(name),
  });

  if (error) {
    return (
      <div className="p-4 bg-destructive/10 border border-destructive rounded-lg flex gap-2">
        <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
        <div>
          <h3 className="font-medium text-destructive">County not found</h3>
        </div>
      </div>
    );
  }

  if (isLoading || !county) {
    return <Skeleton className="h-96 w-full" />;
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">{county.name} County</h1>
      </div>

      {/* Governor */}
      <section className="p-6 rounded-lg border bg-card space-y-4">
        <h2 className="text-2xl font-bold">Governor</h2>
        <div className="space-y-2">
          <p className="text-xl font-semibold">{county.governor_name}</p>
          <p className="text-muted-foreground">{county.governor_party}</p>
        </div>
      </section>

      {/* Senators */}
      {county.senators_json && county.senators_json.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Senators ({county.senators_json.length})</h2>
          <div className="grid gap-4">
            {county.senators_json.map((senator, idx) => (
              <div key={idx} className="p-4 rounded-lg border bg-card">
                <p className="font-semibold">{senator.name}</p>
                <p className="text-sm text-muted-foreground">{senator.party}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* MPs */}
      {county.mps_json && county.mps_json.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Members of Parliament ({county.mps_json.length})</h2>
          <div className="grid gap-4">
            {county.mps_json.map((mp, idx) => (
              <div key={idx} className="p-4 rounded-lg border bg-card">
                <p className="font-semibold">{mp.name}</p>
                <p className="text-sm text-muted-foreground">{mp.constituency}</p>
                <p className="text-sm text-muted-foreground">{mp.party}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Voted Bills */}
      {county.voted_bills_json && county.voted_bills_json.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Voted Bills</h2>
          <div className="grid gap-4">
            {county.voted_bills_json.map((bill, idx) => (
              <div key={idx} className="p-4 rounded-lg border bg-card space-y-2">
                <p className="font-semibold">{bill.bill_title}</p>
                <div className="flex gap-4 text-sm text-muted-foreground">
                  <span>
                    <strong>Vote:</strong> {bill.vote}
                  </span>
                  <span>
                    <strong>Date:</strong> {bill.date}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Past Election Results */}
      {county.past_election_results_json && county.past_election_results_json.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Election Results</h2>
          <div className="grid gap-4">
            {county.past_election_results_json.map((result, idx) => (
              <div key={idx} className="p-4 rounded-lg border bg-card">
                <p className="font-semibold">
                  {result.year} {result.type.replace('_', ' ')}
                </p>
                <p className="text-muted-foreground">Winner: {result.winner}</p>
                {result.votes && <p className="text-sm text-muted-foreground">Votes: {result.votes.toLocaleString()}</p>}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
