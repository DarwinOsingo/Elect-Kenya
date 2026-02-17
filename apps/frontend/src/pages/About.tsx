export default function AboutPage() {
  return (
    <div className="max-w-2xl space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">About Elect 2027</h1>
      </div>

      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Our Mission</h2>
        <p className="leading-relaxed">
          Elect 2027 is an independent, non-partisan educational platform designed to empower Kenyan voters with accurate,
          balanced information about candidates, policies, and electoral integrity risks in the 2027 general elections.
        </p>
      </section>

      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Our Values</h2>
        <ul className="space-y-3">
          {[
            {
              title: 'Independence',
              desc: 'We have no affiliation with political parties, IEBC, or government bodies.',
            },
            {
              title: 'Accuracy',
              desc: 'All information is sourced from public records, official statements, and reputable media.',
            },
            {
              title: 'Balance',
              desc: 'We present multiple perspectives on key issues without bias toward any candidate or party.',
            },
            {
              title: 'Transparency',
              desc: 'We cite sources and encourage users to verify claims independently.',
            },
          ].map((value, idx) => (
            <div key={idx}>
              <p className="font-semibold">{value.title}</p>
              <p className="text-muted-foreground">{value.desc}</p>
            </div>
          ))}
        </ul>
      </section>

      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Data Sources</h2>
        <ul className="space-y-2 text-sm">
          <li>• Official websites of candidates and political parties</li>
          <li>• Wikipedia (for biographical information—always verified independently)</li>
          <li>• Parliament.go.ke and Senate.go.ke (for voting records)</li>
          <li>• IEBC (Independent Electoral and Boundaries Commission)</li>
          <li>• Media reports from established news outlets</li>
          <li>• EACC (Ethics and Anti-Corruption Commission) reports</li>
          <li>• Transparency International Kenya studies</li>
        </ul>
      </section>

      <section className="space-y-4">
        <h2 className="text-2xl font-bold">How to Use This Site</h2>
        <ol className="space-y-3 list-decimal list-inside">
          <li>
            <strong>Explore Candidates:</strong> Learn about presidential candidates, their policies, achievements, and
            controversies.
          </li>
          <li>
            <strong>Understand Issues:</strong> Read balanced perspectives on economy, healthcare, education, and corruption.
          </li>
          <li>
            <strong>Know Vote-Buying Risks:</strong> Understand how vote-buying works and the real cost of taking bribes.
          </li>
          <li>
            <strong>Explore Counties:</strong> Find who represents you at gubernatorial, senatorial, and parliamentary levels.
          </li>
          <li>
            <strong>Verify Everything:</strong> Use the sources cited to fact-check claims on official websites.
          </li>
        </ol>
      </section>

      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Limitations & Disclaimers</h2>
        <ul className="space-y-2 text-sm">
          <li>• This site is not affiliated with IEBC, any political party, or government body.</li>
          <li>• Information is current as of the last update; some details may evolve.</li>
          <li>• Wikipedia summaries are community-edited; always verify claims against primary sources.</li>
          <li>• All users should independently verify claims using official sources before forming political views.</li>
        </ul>
      </section>

      <section className="p-6 bg-blue-50 dark:bg-blue-950 rounded-lg border border-blue-200 dark:border-blue-800">
        <h3 className="font-bold text-blue-900 dark:text-blue-100 mb-2">Questions or Feedback?</h3>
        <p className="text-sm text-blue-900 dark:text-blue-100">
          If you find inaccuracies, outdated information, or have suggestions, please contact us. We're committed to making this
          resource as helpful and accurate as possible.
        </p>
      </section>
    </div>
  );
}
