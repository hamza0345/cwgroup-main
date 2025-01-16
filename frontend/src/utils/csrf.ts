// Function to extract a specific cookie value by name
export function getCookie(name: string): string {
  const matches = document.cookie.match(
    new RegExp(
      `(?:^|; )${name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1')}=([^;]*)`
    )
  );
  return matches ? decodeURIComponent(matches[1]) : '';
}

// Function to get the CSRF token from cookies
export function getCsrfToken(): string {
  return getCookie('csrftoken');
}
