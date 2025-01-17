// basically gets the csrf fom the cookies then returns it
export function getCookie(name: string): string {
  const matches = document.cookie.match(
    new RegExp(
      `(?:^|; )${name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1')}=([^;]*)`
    )
  );
  return matches ? decodeURIComponent(matches[1]) : '';
}

//  get the CSRF token from cookies
export function getCsrfToken(): string {
  return getCookie('csrftoken');
}
