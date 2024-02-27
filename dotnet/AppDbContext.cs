namespace ClientApi;

using Microsoft.EntityFrameworkCore;
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Client> Client { get; set; }
    public DbSet<Transaction> Transaction { get; set; }
}