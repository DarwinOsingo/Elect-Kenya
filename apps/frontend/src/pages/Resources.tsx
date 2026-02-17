export default function ResourcesPage() {
  const resources = [
    {
      category: 'Electoral Information',
      items: [
        { title: 'IEBC Official Website', url: 'https://www.iebc.or.ke' },
        { title: 'Kenya Parliament', url: 'https://www.parliament.go.ke' },
        { title: 'Kenya Senate', url: 'https://www.senate.go.ke' },
      ],
    },
    {
      category: 'Transparency & Accountability',
      items: [
        { title: 'EACC (Ethics & Anti-Corruption Commission)', url: 'https://www.eacc.go.ke' },
        { title: 'Transparency International Kenya', url: 'https://www.tikenya.org' },
        { title: 'Kenya Human Rights Commission', url: 'https://www.khrc.or.ke' },
      ],
    },
    {
      category: 'Media & News',
      items: [
        { title: 'BBC Africa', url: 'https://www.bbc.com/news/world/africa' },
        { title: 'Reuters', url: 'https://www.reuters.com' },
        { title: 'Al Jazeera', url: 'https://www.aljazeera.com' },
        { title: 'The East African', url: 'https://www.theeastafrican.co.ke' },
      ],
    },
    {
      category: 'Voter Education',
      items: [
        { title: 'IFES (International Foundation for Electoral Systems)', url: 'https://www.ifes.org' },
        { title: 'International IDEA', url: 'https://www.idea.int' },
      ],
    },
  ];

  return (
    <div className="max-w-3xl space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Resources & References</h1>
        <p className="text-lg text-muted-foreground">
          Trusted sources for election information, transparency, and voter education.
        </p>
      </div>

      {resources.map((section, idx) => (
        <section key={idx} className="space-y-4">
          <h2 className="text-2xl font-bold">{section.category}</h2>
          <div className="space-y-2">
            {section.items.map((item, sidx) => (
              <a
                key={sidx}
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block p-4 rounded-lg border bg-card hover:border-primary hover:bg-primary/5 transition-colors"
              >
                <p className="font-medium text-primary hover:underline">{item.title}</p>
                <p className="text-xs text-muted-foreground break-all">{item.url}</p>
              </a>
            ))}
          </div>
        </section>
      ))}

      {/* Tips for Fact-Checking */}
      <section className="space-y-4 p-6 bg-blue-50 dark:bg-blue-950 rounded-lg border border-blue-200 dark:border-blue-800">
        <h2 className="text-2xl font-bold text-blue-900 dark:text-blue-100">Tips for Fact-Checking</h2>
        <ol className="space-y-2 text-sm text-blue-900 dark:text-blue-100 list-decimal list-inside">
          <li>Check multiple sources before believing a claim.</li>
          <li>Look for primary sources (official statements, court documents) rather than secondhand reports.</li>
          <li>Be skeptical of claims without dates, names, or citations.</li>
          <li>Use snopes.com, Politifact, or Africa Check for debunking urban myths.</li>
          <li>When in doubt, visit official government websites or established news archives.</li>
          <li>Ask: Who benefits from this story? Could it be propaganda or misinformation?</li>
        </ol>
      </section>

      {/* Reporting */}
      <section className="space-y-4 p-6 bg-green-50 dark:bg-green-950 rounded-lg border border-green-200 dark:border-green-800">
        <h2 className="text-2xl font-bold text-green-900 dark:text-green-100">Reporting Problems</h2>
        <p className="text-sm text-green-900 dark:text-green-100 mb-3">
          If you encounter electoral violations or malpractices:
        </p>
        <ul className="space-y-2 text-sm text-green-900 dark:text-green-100">
          <li>
            <strong>Vote-Buying:</strong> Report to IEBC Voter Hotline or election observers
          </li>
          <li>
            <strong>Corruption:</strong> Report to EACC (https://www.eacc.go.ke/report/)
          </li>
          <li>
            <strong>Human Rights Violations:</strong> Report to Kenya Human Rights Commission
          </li>
          <li>
            <strong>Electoral Discrepancies:</strong> Contact IEBC directly
          </li>
        </ul>
      </section>
    </div>
  );
}
