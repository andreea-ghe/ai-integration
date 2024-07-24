async function postCommentToGitHub(escaped_comments, commit_id, file_path, start_line, side) {
  const { Octokit } = await import('@octokit/core');
  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

  const [owner, repo] = process.env.GITHUB_REPOSITORY.split('/');

  const response = await octokit.request('POST /repos/{owner}/{repo}/pulls/{pull_number}/comments', {
    owner: owner,
    repo: repo,
    pull_number: process.env.GITHUB_EVENT_NUMBER,
    body: escaped_comments,
    commit_id: commit_id,
    path: file_path,
    position: parseInt(start_line),
    side: side,
    subject_type: 'line',
    in_reply_to: null,
    headers: {
      'X-GitHub-Api-Version': '2022-11-28'
    }
  });

  console.log(JSON.parse(response));
  
  if (!response.ok) {
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
