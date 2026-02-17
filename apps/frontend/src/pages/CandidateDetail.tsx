import { useParams } from '@tanstack/react-router';
import { useQuery } from '@tanstack/react-query';
import API from '../lib/api';
import { Candidate } from '@elect/shared';
import { Skeleton } from '../components/ui/Skeleton';
import { AlertCircle, ExternalLink, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';

async function fetchCandidate(slug: string): Promise<Candidate> {
  const { data } = await API.get(`/candidates/${slug}`);
  return data;
}

export default function CandidateDetailPage() {
  const { slug } = useParams({ from: '/candidates/$slug' });
  const { data: candidate, isLoading, error } = useQuery({
    queryKey: ['candidate', slug],
    queryFn: () => fetchCandidate(slug),
  });

  if (error) {
    return (
      <div className="space-y-6">
        <div className="p-4 bg-destructive/10 border border-destructive rounded-lg flex gap-2">
          <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-destructive">Candidate not found</h3>
            <p className="text-sm text-muted-foreground">
              {error instanceof Error ? error.message : 'This candidate could not be loaded.'}
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (isLoading || !candidate) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-12 w-3/4" />
        <Skeleton className="h-96 w-full" />
        <Skeleton className="h-24 w-full" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
          <h1 className="text-4xl font-bold mb-2">{candidate.name}</h1>
          <p className="text-xl text-primary font-medium mb-4">{candidate.party}</p>
          {candidate.county_affiliation && (
            <p className="text-muted-foreground">County Affiliation: {candidate.county_affiliation}</p>
          )}
        </div>
        {candidate.photo_url && (
          <div className="hidden md:block">
            <img
              src={candidate.photo_url}
              alt={candidate.name}
              className="w-full rounded-lg border shadow-lg"
            />
          </div>
        )}
      </div>

      {/* Bio Section */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Biography</h2>
        <p className="leading-relaxed text-lg">{candidate.bio_text}</p>

        {/* Wikipedia Section */}
        <div className="p-4 bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg">
          <p className="text-sm text-blue-900 dark:text-blue-100">
            <strong>Note:</strong> Additional information sourced from Wikipedia (live, community-edited). Always verify independently
            using official sources.
          </p>
        </div>
      </section>

      {/* Policies */}
      {candidate.policies_json && candidate.policies_json.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Key Policies & Promises</h2>
          <div className="space-y-3">
            {candidate.policies_json.map((policy, idx) => (
              <div key={idx} className="p-4 border rounded-lg space-y-2">
                <h3 className="font-semibold text-lg">{policy.promise}</h3>
                <p className="text-muted-foreground">{policy.details}</p>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium">Progress:</span>
                  <span
                    className={`text-sm px-2 py-1 rounded ${
                      policy.progress === 'completed'
                        ? 'bg-green-100 dark:bg-green-900 text-green-900 dark:text-green-100'
                        : policy.progress === 'in_progress'
                          ? 'bg-yellow-100 dark:bg-yellow-900 text-yellow-900 dark:text-yellow-100'
                          : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
                    }`}
                  >
                    {policy.progress.replace('_', ' ')}
                  </span>
                </div>
                {policy.sources && policy.sources.length > 0 && (
                  <div className="pt-2 border-t">
                    <p className="text-xs font-medium text-muted-foreground mb-1">Sources:</p>
                    <ul className="space-y-1">
                      {policy.sources.map((source, sidx) => (
                        <li key={sidx} className="text-xs text-blue-600 dark:text-blue-400 break-all">
                          {source}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Achievements & Controversies */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Good */}
        {candidate.good_json && candidate.good_json.length > 0 && (
          <section className="p-6 border rounded-lg bg-green-50 dark:bg-green-950">
            <div className="flex items-center gap-2 mb-4">
              <CheckCircle2 className="w-5 h-5 text-green-600 dark:text-green-400" />
              <h3 className="text-lg font-bold text-green-900 dark:text-green-100">Achievements</h3>
            </div>
            <ul className="space-y-2">
              {candidate.good_json.map((item, idx) => (
                <li key={idx} className="text-sm text-green-900 dark:text-green-100 flex gap-2">
                  <span className="text-green-600 dark:text-green-400 flex-shrink-0">✓</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Bad */}
        {candidate.bad_json && candidate.bad_json.length > 0 && (
          <section className="p-6 border rounded-lg bg-orange-50 dark:bg-orange-950">
            <div className="flex items-center gap-2 mb-4">
              <XCircle className="w-5 h-5 text-orange-600 dark:text-orange-400" />
              <h3 className="text-lg font-bold text-orange-900 dark:text-orange-100">Controversies</h3>
            </div>
            <ul className="space-y-2">
              {candidate.bad_json.map((item, idx) => (
                <li key={idx} className="text-sm text-orange-900 dark:text-orange-100 flex gap-2">
                  <span className="text-orange-600 dark:text-orange-400 flex-shrink-0">⚠</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Crazy */}
        {candidate.crazy_json && candidate.crazy_json.length > 0 && (
          <section className="p-6 border rounded-lg bg-red-50 dark:bg-red-950">
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400" />
              <h3 className="text-lg font-bold text-red-900 dark:text-red-100">Questionable Claims</h3>
            </div>
            <ul className="space-y-2">
              {candidate.crazy_json.map((item, idx) => (
                <li key={idx} className="text-sm text-red-900 dark:text-red-100 flex gap-2">
                  <span className="text-red-600 dark:text-red-400 flex-shrink-0">❌</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>

      {/* Disclaimer */}
      <section className="p-6 bg-yellow-50 dark:bg-yellow-950 rounded-lg border border-yellow-200 dark:border-yellow-800">
        <h3 className="font-semibold text-yellow-900 dark:text-yellow-100 mb-2">
          📋 Verification Reminder
        </h3>
        <p className="text-sm text-yellow-800 dark:text-yellow-200">
          This information is compiled from public sources. We encourage you to verify all claims independently using official
          sources, candidate websites, and reputable media outlets. Accuracy is important to us, but information can evolve.
        </p>
      </section>
    </div>
  );
}
