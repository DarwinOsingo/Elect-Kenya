import { useQuery } from '@tanstack/react-query';
import API from '../lib/api';
import { VoteBuyingFact } from '@elect/shared';
import { Skeleton } from '../components/ui/Skeleton';
import { AlertCircle, AlertTriangle } from 'lucide-react';

async function fetchVoteBuyingFacts(): Promise<VoteBuyingFact[]> {
  const { data } = await API.get('/vote-buying-facts');
  return data;
}

export default function VoteBuyingPage() {
  const { data: facts, isLoading, error } = useQuery({
    queryKey: ['vote-buying-facts'],
    queryFn: fetchVoteBuyingFacts,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold mb-2">Understanding Vote-Buying & Election Malpractices</h1>
        <p className="text-lg text-muted-foreground">
          Learn how vote-buying works, its impacts, and how to protect yourself and your vote.
        </p>
      </div>

      {/* Warning Banner */}
      <div className="p-6 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg flex gap-4">
        <AlertTriangle className="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0" />
        <div>
          <h3 className="font-bold text-red-900 dark:text-red-100 mb-2">Your Vote Has Dignity</h3>
          <p className="text-sm text-red-900 dark:text-red-100">
            Vote-buying violates your right to free and fair elections. Short-term bribes (KSh 50–1,000) pale in comparison to
            what corruption costs your country over years: lost healthcare, education, infrastructure, and economic opportunity.
          </p>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-destructive/10 border border-destructive rounded-lg flex gap-2">
          <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-destructive">Failed to load information</h3>
          </div>
        </div>
      )}

      {isLoading ? (
        <div className="space-y-6">
          {Array.from({ length: 4 }).map((_, i) => (
            <Skeleton key={i} className="h-40 w-full" />
          ))}
        </div>
      ) : (
        <div className="space-y-6">
          {facts?.map((fact) => (
            <div key={fact.id} className="p-6 rounded-lg border bg-card space-y-4">
              <h2 className="text-2xl font-bold">{fact.section_title}</h2>
              <p className="leading-relaxed whitespace-pre-wrap text-muted-foreground">{fact.content_text}</p>

              {fact.sources_json && fact.sources_json.length > 0 && (
                <div className="pt-4 border-t space-y-2">
                  <h3 className="font-semibold text-sm">References:</h3>
                  <ul className="space-y-1">
                    {fact.sources_json.map((source, idx) => (
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

      {/* Action Items */}
      <section className="p-6 bg-blue-50 dark:bg-blue-950 rounded-lg border border-blue-200 dark:border-blue-800 space-y-4">
        <h3 className="text-2xl font-bold text-blue-900 dark:text-blue-100">How to Protect Your Vote</h3>
        <ul className="space-y-2 text-sm text-blue-900 dark:text-blue-100">
          <li className="flex gap-2">
            <span className="font-bold">1.</span>
            <span>Refuse any inducements before, during, and after elections.</span>
          </li>
          <li className="flex gap-2">
            <span className="font-bold">2.</span>
            <span>Report vote-buying to election observers or the IEBC verification line.</span>
          </li>
          <li className="flex gap-2">
            <span className="font-bold">3.</span>
            <span>Vote for candidates based on policies, track record, and integrity—not bribes.</span>
          </li>
          <li className="flex gap-2">
            <span className="font-bold">4.</span>
            <span>Encourage family and friends to do the same.</span>
          </li>
          <li className="flex gap-2">
            <span className="font-bold">5.</span>
            <span>Report suspected electoral offenses to proper authorities.</span>
          </li>
        </ul>
      </section>
    </div>
  );
}
