document.addEventListener('DOMContentLoaded', () => {
    const teamSelect = document.getElementById('team-select');
    const scoutingForm = document.getElementById('scouting-form');
    const reportContainer = document.getElementById('report-container');
    const API_BASE_URL = 'http://localhost:8000';

    // Fetch teams and populate the dropdown
    fetch(`${API_BASE_URL}/api/teams/`)
        .then(response => response.json())
        .then(data => {
            data.forEach(team => {
                const option = document.createElement('option');
                option.value = team.id;
                option.textContent = team.name;
                teamSelect.appendChild(option);
            });
        });

    // Handle form submission
    scoutingForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const teamId = teamSelect.value;
        if (!teamId) return;

        fetch(`${API_BASE_URL}/api/scouting-report/${teamId}`)
            .then(response => response.json())
            .then(report => {
                displayReport(report);
            });
    });

    function displayReport(report) {
        document.getElementById('report-team-name').textContent = `${report.team_name} - Scouting Report`;
        document.getElementById('executive-summary').textContent = report.executive_summary;
        
        const opponentOverview = document.getElementById('opponent-overview');
        opponentOverview.innerHTML = `
            <p><b>Adjusted Offense:</b> ${report.opponent_overview.team_stats.adj_o}</p>
            <p><b>Adjusted Defense:</b> ${report.opponent_overview.team_stats.adj_d}</p>
            <p><b>Tempo:</b> ${report.opponent_overview.team_stats.tempo}</p>
            <p><b>Recent Form:</b> ${report.opponent_overview.recent_form}</p>
            <p><b>Style of Play:</b> ${report.opponent_overview.style_of_play}</p>
        `;

        const keyPlayers = document.getElementById('key-players');
        keyPlayers.innerHTML = report.key_players.map(player => `
            <div>
                <h4>${player.name} (${player.position})</h4>
                <p><b>Stats:</b> PPG: ${player.stats.ppg}, APG: ${player.stats.apg}, RPG: ${player.stats.rpg}</p>
                <p><b>Tendencies:</b> ${player.tendencies}</p>
                <img src="${player.shot_chart_url}" alt="Shot chart for ${player.name}" style="max-width: 100%;">
            </div>
        `).join('');

        const coachingStrategy = document.getElementById('coaching-strategy');
        coachingStrategy.innerHTML = `
            <p><b>Offensive Sets:</b> ${report.coaching_strategy.offensive_sets}</p>
            <p><b>Defensive Schemes:</b> ${report.coaching_strategy.defensive_schemes}</p>
            <p><b>Philosophy:</b> ${report.coaching_strategy.philosophy}</p>
        `;

        const gameDayFactors = document.getElementById('game-day-factors');
        gameDayFactors.innerHTML = `
            <p><b>Injuries:</b> ${report.game_day_factors.injuries}</p>
            <p><b>Travel Impact:</b> ${report.game_day_factors.travel_impact}</p>
            <p><b>Venue Performance:</b> ${report.game_day_factors.venue_performance}</p>
        `;

        document.getElementById('nil-roster-dynamics').textContent = report.nil_roster_dynamics;
        document.getElementById('warrior-mentality-focus').textContent = report.warrior_mentality_focus;

        document.getElementById('raw-data').textContent = `hoopR: ${report.hoopr_data}\n\ntoRvik: ${report.torvik_data}`;

        reportContainer.classList.remove('hidden');
    }
});