export default function WhatCouldHaveBeenPage() {
  const totalCorruptionLossKSh = 5_000_000_000_000; // KSh 5 trillion est. over 10 years
  const hospitalUnitCostUSD = 3_500_000; // Average hospital construction
  const classroomUnitCostUSD = 100_000; // Basic classroom
  const roadKMUnitCostUSD = 600_000; // Road construction
  const exchangeRate = 130; // KSh to USD

  const calculations = [
    {
      title: 'Public Hospitals',
      emoji: '🏥',
      description: 'State-of-the-art teaching hospitals',
      unitCost: hospitalUnitCostKSh = hospitalUnitCostUSD * exchangeRate,
      possible: Math.floor((totalCorruptionLossKSh * 0.3) / (hospitalUnitCostUSD * exchangeRate)),
      icon: '🏥',
    },
    {
      title: 'Schools Built',
      emoji: '🏫',
      description: 'Primary and secondary schools with labs',
      unitCost: classroomUnitCostUSD * exchangeRate,
      possible: Math.floor((totalCorruptionLossKSh * 0.3) / (classroomUnitCostUSD * exchangeRate)),
      icon: '🏫',
    },
    {
      title: 'Roads',
      emoji: '🛣️',
      description: 'Modern paved roads (km)',
      unitCost: roadKMUnitCostUSD * exchangeRate,
      possible: Math.floor((totalCorruptionLossKSh * 0.2) / (roadKMUnitCostUSD * exchangeRate)),
      icon: '🛣️',
    },
    {
      title: 'Debt Reduction',
      emoji: '💰',
      description: 'National debt interest savings',
      unitCost: 1,
      possible: totalCorruptionLossKSh * 0.2,
      isMoneyAmount: true,
      icon: '💰',
    },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">What Could Have Been...</h1>
        <p className="text-lg text-muted-foreground">
          If corruption had been eliminated: An estimate of what Kenya could have built and achieved over the past decade.
        </p>
      </div>

      {/* Main Stat */}
      <section className="p-8 bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-950 dark:to-orange-950 border border-orange-200 dark:border-orange-800 rounded-lg">
        <p className="text-sm text-muted-foreground mb-2">Estimated Corruption Losses (10 Years)</p>
        <p className="text-5xl font-bold text-orange-700 dark:text-orange-300 mb-2">
          KSh {(totalCorruptionLossKSh / 1_000_000_000_000).toFixed(1)}T
        </p>
        <p className="text-muted-foreground">
          Estimated annual losses from corruption across all government sectors. Sources: Transparency International Kenya,
          EACC reports.
        </p>
      </section>

      {/* Impact Grid */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {calculations.map((item, idx) => (
          <div key={idx} className="p-6 rounded-lg border bg-card space-y-4">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-2xl font-bold">{item.title}</h3>
                <p className="text-sm text-muted-foreground">{item.description}</p>
              </div>
              <span className="text-4xl">{item.emoji}</span>
            </div>

            <div className="pt-4 border-t">
              <p className="text-sm text-muted-foreground mb-1">Could Have Built:</p>
              <p className="text-3xl font-bold text-primary">
                {item.isMoneyAmount
                  ? `KSh ${(item.possible / 1_000_000_000).toFixed(0)}B`
                  : item.possible.toLocaleString()}
              </p>
            </div>

            {!item.isMoneyAmount && (
              <div className="pt-2 text-xs text-muted-foreground">
                <p>
                  @ KSh {(item.unitCost / 1_000_000).toFixed(0)}M per {item.title === 'Roads' ? 'km' : 'unit'}
                </p>
              </div>
            )}
          </div>
        ))}
      </section>

      {/* Breakdown */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold">How This Corruption Happened</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            {
              sector: 'Government Contracts',
              percentage: 35,
              description: 'Inflated bids, kickbacks to officials',
            },
            {
              sector: 'Land & Real Estate',
              percentage: 25,
              description: 'Illegal land grabs, undervaluation',
            },
            {
              sector: 'Public Works',
              percentage: 20,
              description: 'Substandard materials, non-completion',
            },
            {
              sector: 'Healthcare & Education',
              percentage: 15,
              description: 'Missing medicines, ghost teachers, phantom schools',
            },
            {
              sector: 'Revenue Leakage',
              percentage: 3,
              description: 'Tax evasion, underreporting of revenue',
            },
            {
              sector: 'Other',
              percentage: 2,
              description: 'Misallocation of public funds',
            },
          ].map((item, idx) => (
            <div key={idx} className="p-4 border rounded-lg">
              <div className="flex justify-between items-center mb-2">
                <h4 className="font-semibold">{item.sector}</h4>
                <span className="text-lg font-bold text-primary">{item.percentage}%</span>
              </div>
              <p className="text-sm text-muted-foreground">{item.description}</p>
              <div className="mt-3 w-full bg-muted rounded-full h-2">
                <div
                  className="bg-primary h-2 rounded-full transition-all"
                  style={{ width: `${item.percentage}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Call to Action */}
      <section className="p-6 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 rounded-lg">
        <h3 className="text-2xl font-bold text-green-900 dark:text-green-100 mb-4">You Can Make a Difference</h3>
        <ul className="space-y-2 text-sm text-green-900 dark:text-green-100">
          <li>✓ Vote for candidates with strong anti-corruption records</li>
          <li>✓ Support accountability and transparency initiatives</li>
          <li>✓ Report corruption to EACC or Citizen hotlines</li>
          <li>✓ Demand that elected officials publish asset declarations</li>
          <li>✓ Share this information to raise awareness</li>
        </ul>
      </section>

      {/* Disclaimer */}
      <section className="p-4 bg-yellow-50 dark:bg-yellow-950 rounded-lg border border-yellow-200 dark:border-yellow-800">
        <p className="text-xs text-yellow-800 dark:text-yellow-200">
          <strong>Methodological Note:</strong> These are estimates based on EACC, TI Kenya, and World Bank reports. Actual figures
          vary year to year. This analysis is for educational purposes to illustrate the opportunity cost of corruption.
        </p>
      </section>
    </div>
  );
}
