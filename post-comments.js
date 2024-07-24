import { Octokit } from '@octokit/core';

async function postCommentToGitHub(escaped_comments, commit_id, file_path, start_line, side) {
  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
  
  console.log(escaped_comments);
  console.log(commit_id);
  console.log(file_path);
  console.log(start_line);
  console.log(side);
  
  const [owner, repo] = process.env.GITHUB_REPOSITORY.split('/');

  const response = await octokit.request('POST /repos/{owner}/{repo}/pulls/{pull_number}/comments', {
    owner,
    repo,
    pull_number: process.env.GITHUB_EVENT_NUMBER,
    commit_id,
    path: file_path,
    body: escaped_comments,
    side,
    line: parseInt(start_line),
    start_side: 'RIGHT', // Use 'RIGHT' for the default side
    position: parseInt(start_line),
    headers: {
      'X-GitHub-Api-Version': '2022-11-28'
    }
  });

  if (response.status !== 201) {
    throw new Error(`GitHub API responded with ${response.status}: ${response.statusText}`);
  }

  return response.data;
}

const args = process.argv.slice(2);

if (args.length < 5) {
  console.error('Insufficient arguments. Expected: escaped_comments, commit_id, file_path, start_line, side');
  process.exit(1);
}

const [escaped_comments, commit_id, file_path, start_line, side] = args;

postCommentToGitHub(escaped_comments, commit_id, file_path, start_line, side)
  .then(response => console.log('Comment posted successfully:', response))
  .catch(error => console.error('Error posting comment:', error));
