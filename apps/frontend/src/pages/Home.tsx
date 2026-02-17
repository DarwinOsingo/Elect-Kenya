export default function HomePage() {
  return (
    <div className="space-y-8">
      {/* Hero */}
      <section className="text-center py-12">
        <h1 className="text-4xl sm:text-5xl font-bold mb-4">
          Make an Informed Choice in 2027
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Access balanced, sourced information on candidates, policies, and the risks of vote-buying.
          Vote for change, not for bribes.
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <a
            href="/candidates"
            className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-medium hover:opacity-90 transition"
          >
            Explore Candidates
          </a>
          <a
            href="/vote-buying"
            className="px-6 py-3 border border-primary text-primary rounded-lg font-medium hover:bg-primary hover:text-primary-foreground transition"
          >
            Understand Vote-Buying
          </a>
        </div>
      </section>

      {/* Info Sections */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[
          {
            title: 'Know Your Candidates',
            emoji: '👥',
            description: 'Learn about presidential, gubernatorial, and parliamentary candidates.',
          },
          {
            title: 'Understand the Issues',
            emoji: '💼',
            description: 'Explore key policy areas: economy, healthcare, education, corruption.',
          },
          {
            title: 'Protect Your Vote',
            emoji: '🛡️',
            description: 'Understand vote-buying tactics and stay informed about electoral integrity.',
          },
        ].map((item) => (
          <div key={item.title} className="p-6 rounded-lg border bg-card">
            <div className="text-4xl mb-3">{item.emoji}</div>
            <h3 className="text-lg font-semibold mb-2">{item.title}</h3>
            <p className="text-muted-foreground text-sm">{item.description}</p>
          </div>
        ))}
      </section>

      {/* Disclaimer */}
      <section className="p-6 bg-yellow-50 dark:bg-yellow-950 rounded-lg border border-yellow-200 dark:border-yellow-800">
        <h3 className="font-semibold text-yellow-900 dark:text-yellow-100 mb-2">
          📋 Independent & Non-Partisan
        </h3>
        <p className="text-sm text-yellow-800 dark:text-yellow-200">
          This site is an independent educational resource not affiliated with IEBC, any political party, or government body.
          All information should be verified independently. We strive for accuracy but encourage you to fact-check claims using
          official sources.
        </p>
      </section>
    </div>
  );
}
