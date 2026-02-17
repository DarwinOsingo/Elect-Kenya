import { useQuery } from '@tanstack/react-query';
import { Link } from '@tanstack/react-router';
import API from '../lib/api';
import { Candidate } from '@elect/shared';
import { Skeleton } from '../components/ui/Skeleton';
import { AlertCircle } from 'lucide-react';

async function fetchCandidates(): Promise<Candidate[]> {
  const { data } = await API.get('/candidates');
  return data;
}

export default function CandidatesPage() {
  const { data: candidates, isLoading, error } = useQuery({
    queryKey: ['candidates'],
    queryFn: fetchCandidates,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold mb-2">2027 Presidential Candidates</h1>
        <p className="text-lg text-muted-foreground">
          Explore detailed information, policies, and achievements of candidates.
        </p>
      </div>

      {error && (
        <div className="p-4 bg-destructive/10 border border-destructive rounded-lg flex gap-2">
          <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-destructive">Failed to load candidates</h3>
            <p className="text-sm text-muted-foreground">
              {error instanceof Error ? error.message : 'Please try again later.'}
            </p>
          </div>
        </div>
      )}

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="p-6 rounded-lg border bg-card space-y-4">
              <Skeleton className="h-48 w-full" />
              <Skeleton className="h-6 w-3/4" />
              <Skeleton className="h-4 w-1/2" />
            </div>
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {candidates?.map((candidate) => (
            <Link
              key={candidate.slug}
              to={`/candidates/${candidate.slug}`}
              className="group p-6 rounded-lg border border-border bg-card hover:border-primary hover:shadow-lg transition-all"
            >
              {candidate.photo_url && (
                <img
                  src={candidate.photo_url}
                  alt={candidate.name}
                  className="w-full h-48 object-cover rounded-lg mb-4 group-hover:opacity-90 transition"
                  loading="lazy"
                />
              )}
              <h3 className="text-xl font-semibold mb-1 group-hover:text-primary transition">
                {candidate.name}
              </h3>
              <p className="text-sm text-muted-foreground mb-3">{candidate.party}</p>
              <p className="text-sm line-clamp-3">{candidate.bio_text}</p>
              <div className="mt-4 flex items-center text-sm font-medium text-primary group-hover:underline">
                View Full Profile →
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
