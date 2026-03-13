export function formatDate(date: Date, locale: string = 'en-US'): string {
    return new Intl.DateTimeFormat(locale).format(date);
}

export function formatDateTime(date: Date, locale: string = 'en-US'): string {
    return new Intl.DateTimeFormat(locale, {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
    }).format(date);
}

export function parseDate(dateString: string): Date {
    return new Date(dateString);
}

export function isValidDate(date: Date): boolean {
    return !isNaN(date.getTime());
}