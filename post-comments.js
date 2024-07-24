const fs = require('fs');
const fetch = require('node-fetch');

async function postCommentToGitHub(escaped_comments, commit_id, file_path, start_line, side) {
    const url = `https://api.github.com/repos/${process.env.GITHUB_REPOSITORY}/pulls/${process.env.GITHUB_EVENT_NUMBER}/comments`;
    const body = {
        body: escaped_comments,
        commit_id: commit_id,
        path: file_path,
        line: start_line,
        side: side
    };
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/vnd.github+json',
            'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
            'X-GitHub-Api-Version': '2022-11-28'
        },
        body: JSON.stringify(body)
    });
    if (!response.ok) {
        throw new Error(`GitHub API responded with ${response.status}: ${response.statusText}`);
    }
    const data = await response.json();
    return data;
}

async function main() {
    const commit_id = process.env.COMMIT_ID;
    const reviews = fs.readFileSync('reviews.txt', 'utf8').split('\n');

    let file_names = [];
    let diff = '';
    let review = '';
    for (let line of reviews) {
        if (line.startsWith('FILE: ')) {
            file_names.push(line.slice(6));
        } else if (line.startsWith('DIFF: ')) {
            diff = '';
            while ((line = reviews.shift()) !== 'ENDDIFF') {
                diff += `${line}\n`;
            }
        } else if (line.startsWith('REVIEW: ')) {
            review = '';
            while ((line = reviews.shift()) !== 'ENDREVIEW') {
                review += `${line}\n`;
            }

            const hunk_header = diff.match(/@@ -(\d+),(\d+) \+(\d+),(\d+) @@/);
            if (!hunk_header) {
                throw new Error('Failed to parse hunk header');
            }

            const original_start_line = hunk_header[1];
            const new_start_line = hunk_header[3];
            const first_char = diff.charAt(diff.indexOf('@@') + 3);

            let side = '';
            let start_line = '';
            if (first_char === '-') {
                side = 'LEFT';
                start_line = original_start_line;
            } else if (first_char === '+') {
                side = 'RIGHT';
                start_line = new_start_line;
            }

            const file_path = file_names[file_names.length - 1];
            const escaped_comments = JSON.stringify(`${file_path}\n${diff}\n${review}`);
            await postCommentToGitHub(escaped_comments, commit_id, file_path, start_line, side);
        }
    }
}

main().catch(console.error);
