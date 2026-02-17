import { useQuery } from '@tanstack/react-query';
import API from '../lib/api';
import { Issue } from '@elect/shared';
import { Skeleton } from '../components/ui/Skeleton';
import { AlertCircle } from 'lucide-react';

async function fetchIssues(): Promise<Issue[]> {
  const { data } = await API.get('/issues');
  return data;
}

export default function IssuesPage() {
  const { data: issues, isLoading, error } = useQuery({
    queryKey: ['issues'],
    queryFn: fetchIssues,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold mb-2">Key Issues in 2027</h1>
        <p className="text-lg text-muted-foreground">
          Understand the major policy areas and different perspectives on key challenges facing Kenya.
        </p>
      </div>

      {error && (
        <div className="p-4 bg-destructive/10 border border-destructive rounded-lg flex gap-2">
          <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-destructive">Failed to load issues</h3>
          </div>
        </div>
      )}

      {isLoading ? (
        <div className="space-y-6">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-48 w-full" />
          ))}
        </div>
      ) : (
        <div className="space-y-6">
          {issues?.map((issue) => (
            <div key={issue.id} className="p-6 rounded-lg border bg-card space-y-4">
              <h2 className="text-2xl font-bold">{issue.title}</h2>

              {issue.good_points_json && issue.good_points_json.length > 0 && (
                <div className="space-y-2">
                  <h3 className="font-semibold text-green-700 dark:text-green-400">Positive Approaches:</h3>
                  <ul className="space-y-1 text-sm">
                    {issue.good_points_json.map((point, idx) => (
                      <li key={idx} className="flex gap-2">
                        <span className="text-green-600 dark:text-green-400">+</span>
                        <span>{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {issue.bad_points_json && issue.bad_points_json.length > 0 && (
                <div className="space-y-2">
                  <h3 className="font-semibold text-orange-700 dark:text-orange-400">Concerns:</h3>
                  <ul className="space-y-1 text-sm">
                    {issue.bad_points_json.map((point, idx) => (
                      <li key={idx} className="flex gap-2">
                        <span className="text-orange-600 dark:text-orange-400">-</span>
                        <span>{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {issue.sources_json && issue.sources_json.length > 0 && (
                <div className="pt-4 border-t space-y-2">
                  <h3 className="font-semibold text-sm">Sources:</h3>
                  <ul className="space-y-1">
                    {issue.sources_json.map((source, idx) => (
                      <li key={idx} className="text-xs text-blue-600 dark:text-blue-400 break-all">
                        {source}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
