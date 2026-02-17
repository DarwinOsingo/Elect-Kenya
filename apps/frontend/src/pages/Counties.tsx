import { Link } from '@tanstack/react-router';
import { useQuery } from '@tanstack/react-query';
import API from '../lib/api';
import { County } from '@elect/shared';
import { Skeleton } from '../components/ui/Skeleton';

async function fetchCounties(): Promise<County[]> {
  const { data } = await API.get('/counties');
  return data;
}

export default function CountiesPage() {
  const { data: counties, isLoading, error } = useQuery({
    queryKey: ['counties'],
    queryFn: fetchCounties,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold mb-2">Kenya's 47 Counties</h1>
        <p className="text-lg text-muted-foreground">
          Explore gubernatorial, senatorial, and parliamentary representation in each county.
        </p>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-32 w-full" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {counties?.map((county) => (
            <Link
              key={county.id}
              to={`/counties/${county.name}`}
              className="p-6 rounded-lg border bg-card hover:border-primary hover:shadow-lg transition-all group"
            >
              <h3 className="text-xl font-semibold mb-2 group-hover:text-primary transition">
                {county.name}
              </h3>
              <div className="space-y-2 text-sm text-muted-foreground">
                <p>
                  <strong>Governor:</strong> {county.governor_name}
                </p>
                <p>
                  <strong>Party:</strong> {county.governor_party}
                </p>
                <p>
                  <strong>Senators:</strong> {county.senators_json?.length || 0}
                </p>
                <p>
                  <strong>MPs:</strong> {county.mps_json?.length || 0}
                </p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
