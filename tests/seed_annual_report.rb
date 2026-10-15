account = Account.find_by!(username: 'mastodonpy_test', domain: nil)
year = 2025
AnnualReport.new(account, year).generate
report = GeneratedAnnualReport.find_by!(account: account, year: year)

unless Notification.exists?(account: account, type: 'annual_report', activity: report)
  NotifyService.new.call(account, :annual_report, report)
end

unless Notification.exists?(account: account, type: 'annual_report', activity: report)
  abort 'Failed to create the annual report notification'
end

puts "Seeded annual report #{year} and its notification for #{account.username}"
