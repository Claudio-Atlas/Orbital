// Server Component - handles route configuration
export const dynamic = 'force-dynamic';

import ClientComponent from './ClientComponent';

export default function Page() {
  return <ClientComponent />;
}
