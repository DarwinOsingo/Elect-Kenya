import { z } from 'zod';

// Candidate schemas
export const PolicySchema = z.object({
  promise: z.string(),
  details: z.string(),
  progress: z.enum(['not_started', 'in_progress', 'completed']),
  sources: z.array(z.string()),
});

export const CandidateSchema = z.object({
  id: z.number(),
  slug: z.string(),
  name: z.string(),
  party: z.string(),
  photo_url: z.string().url(),
  bio_text: z.string(),
  wiki_title: z.string(),
  good_json: z.array(z.string()),
  bad_json: z.array(z.string()),
  crazy_json: z.array(z.string()),
  policies_json: z.array(PolicySchema),
  county_affiliation: z.string(),
  updated_at: z.string().datetime(),
});

export const CreateCandidateSchema = CandidateSchema.omit({ id: true, updated_at: true });
export const UpdateCandidateSchema = CreateCandidateSchema.partial();

// Issue schemas
export const IssueSchema = z.object({
  id: z.number(),
  title: z.string(),
  good_points_json: z.array(z.string()),
  bad_points_json: z.array(z.string()),
  sources_json: z.array(z.string()),
  updated_at: z.string().datetime(),
});

// Vote-buying schemas
export const VoteBuyingFactSchema = z.object({
  id: z.number(),
  section_title: z.string(),
  content_text: z.string(),
  sources_json: z.array(z.string()),
  updated_at: z.string().datetime(),
});

// County schemas
export const SenatorSchema = z.object({
  name: z.string(),
  party: z.string(),
  wiki_title: z.string(),
});

export const MPSchema = z.object({
  name: z.string(),
  constituency: z.string(),
  party: z.string(),
  wiki_title: z.string(),
});

export const ElectionResultSchema = z.object({
  year: z.number(),
  type: z.enum(['presidential', 'gubernatorial', 'mp']),
  winner: z.string(),
  votes: z.number().optional(),
  source: z.string(),
});

export const VotedBillSchema = z.object({
  bill_title: z.string(),
  bill_id: z.string(),
  vote: z.enum(['Yes', 'No', 'Abstain']),
  date: z.string().date(),
  source_url: z.string().url(),
});

export const CountySchema = z.object({
  id: z.number(),
  name: z.string(),
  governor_name: z.string(),
  governor_party: z.string(),
  governor_wiki_title: z.string(),
  senators_json: z.array(SenatorSchema),
  mps_json: z.array(MPSchema),
  past_election_results_json: z.array(ElectionResultSchema),
  voted_bills_json: z.array(VotedBillSchema),
  updated_at: z.string().datetime(),
});

export const CreateCountySchema = CountySchema.omit({ id: true, updated_at: true });
export const UpdateCountySchema = CreateCountySchema.partial();

// Wikipedia response
export const WikipediaExtractSchema = z.object({
  extract: z.string(),
  thumbnail: z.object({ source: z.string() }).optional(),
  content_urls: z.object({ mobile: z.object({ page: z.string() }) }),
  description: z.string().optional(),
});

export const WikipediaSummarySchema = z.object({
  extract: z.string().optional(),
  thumbnail_url: z.string().optional(),
  page_url: z.string(),
  description: z.string().optional(),
});

// Type exports
export type Policy = z.infer<typeof PolicySchema>;
export type Candidate = z.infer<typeof CandidateSchema>;
export type CreateCandidate = z.infer<typeof CreateCandidateSchema>;
export type UpdateCandidate = z.infer<typeof UpdateCandidateSchema>;

export type Issue = z.infer<typeof IssueSchema>;
export type VoteBuyingFact = z.infer<typeof VoteBuyingFactSchema>;

export type Senator = z.infer<typeof SenatorSchema>;
export type MP = z.infer<typeof MPSchema>;
export type ElectionResult = z.infer<typeof ElectionResultSchema>;
export type VotedBill = z.infer<typeof VotedBillSchema>;
export type County = z.infer<typeof CountySchema>;
export type CreateCounty = z.infer<typeof CreateCountySchema>;
export type UpdateCounty = z.infer<typeof UpdateCountySchema>;

export type WikipediaSummary = z.infer<typeof WikipediaSummarySchema>;
